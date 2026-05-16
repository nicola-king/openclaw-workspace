tech-sharing / 2026-04-15

# Rust 异步运行时 到底在调度什么?

从 Future::poll 到 tokio 的 work-stealing，一次讲清楚。

**@lewis**platform infra · 45 min + Q&A

#async #rust #tokio

agenda.toml

## 今天的路线图

01Context: 为什么需要 async~5min

02Deep dive 1: Future & Waker~12min

03Deep dive 2: Tokio scheduler~15min

04Code: 手写一个 mini-runtime~8min

05Takeaways + Q&A~5min

// context

## 问题：一个线程一个连接， 撑不住 10 万并发。

#### Thread-per-conn

每条连接一根 OS 线程，栈 2–8MB。10 万连接 = 几百 GB RAM。

❌ 不现实

#### Event loop (C)

epoll/kqueue + 回调地狱。快，但写起来痛苦且容易出 bug。

😩 callback hell

#### Async / await

看起来像同步代码，编译成状态机。一根线程跑几千任务。

✅ Rust 选这个

deep-dive · 1 / 2

## Future 其实只有一个方法。

编译器把 async fn 变成一个实现了 Future trait 的匿名状态机。运行时只做一件事：反复 poll 它，直到返回 Ready。

Pending Ready(T) Waker.wake()

future.rs

```
pub trait Future {
    type Output;
    fn poll(
        self: Pin<&mut Self>,
        cx: &mut Context<'_>,
    ) -> Poll<Self::Output>;
}

// Poll::Pending   → 挂起，等 waker 唤醒
// Poll::Ready(v)  → 完成，产出 v
```

deep-dive · 2 / 2

## Tokio 是一个偷任务的小工。

Multi-thread runtime = N 个 worker，每个 worker 有自己的本地队列。空闲的 worker 会去别人队列里"偷"任务。

✦ local queue · 256 slots

✦ global injection queue

✦ work-stealing @ 50% steal ratio

✦ LIFO slot for cache locality

#### scheduler tick loop

1. pop from LIFO slot

2. else pop from local queue

3. else drain global queue (every 61 ticks)

4. else steal from random victim

5. else park the thread

mini-runtime.rs · ~40 LOC

## 手写一个最小 runtime。

src/main.rs

```
use std::collections::VecDeque;
use std::sync::{Arc, Mutex};
use std::task::{Context, Poll, Wake, Waker};

struct Task(Mutex<Pin<Box<dyn Future<Output = ()> + Send>>>);

impl Wake for Task {
    fn wake(self: Arc<Self>) { QUEUE.lock().unwrap().push_back(self); }
}

fn block_on<F: Future<Output = ()> + Send + 'static>(fut: F) {
    spawn(fut);
    while let Some(task) = QUEUE.lock().unwrap().pop_front() {
        let waker = Waker::from(task.clone());
        let mut cx = Context::from_waker(&waker);
        let mut fut = task.0.lock().unwrap();
        let _ = fut.as_mut().poll(&mut cx); // 就是这一行
    }
}
```

// takeaways

## 三件事带回去。

#### 1 · async 是零成本抽象

编译成状态机，没有运行时虚表，没有 GC。

#### 2 · Waker 是脉搏

Future 不主动做事，运行时靠 waker 决定"什么时候再 poll"。

#### 3 · 别在 async 里阻塞

一行 std::fs::read 能让整个 worker 停摆。用 spawn\_blocking。

延伸阅读：tokio.rs/blog/2019-10-scheduler · rust-lang.github.io/async-book

?

## Questions?

github.com/lewis · @lewis on slack

slides: git.co/rt-deck
code: git.co/mini-rt