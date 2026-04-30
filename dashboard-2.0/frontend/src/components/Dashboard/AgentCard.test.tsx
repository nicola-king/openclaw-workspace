import { render, screen } from '@testing-library/react'
import { describe, it, expect } from 'vitest'
import AgentCard from './AgentCard'

describe('AgentCard', () => {
  it('渲染 Agent 名称', () => {
    render(<AgentCard name="太一" status="running" tasks={12} health={98} />)
    expect(screen.getByText('太一')).toBeInTheDocument()
  })

  it('显示正确状态 (运行中)', () => {
    render(<AgentCard name="太一" status="running" tasks={12} health={98} />)
    expect(screen.getByText('运行中')).toBeInTheDocument()
  })

  it('显示正确状态 (空闲)', () => {
    render(<AgentCard name="罔两" status="idle" tasks={0} health={100} />)
    expect(screen.getByText('空闲')).toBeInTheDocument()
  })

  it('显示健康度', () => {
    render(<AgentCard name="太一" status="running" tasks={12} health={98} />)
    expect(screen.getByText('98%')).toBeInTheDocument()
  })

  it('显示任务数', () => {
    render(<AgentCard name="太一" status="running" tasks={12} health={98} />)
    expect(screen.getByText('12 进行中')).toBeInTheDocument()
  })

  it('健康度 >= 95 显示绿色', () => {
    const { container } = render(<AgentCard name="太一" status="running" tasks={12} health={98} />)
    const healthText = container.querySelector('.text-success-green')
    expect(healthText).toBeInTheDocument()
  })

  it('健康度 < 95 显示黄色', () => {
    const { container } = render(<AgentCard name="知几" status="running" tasks={8} health={92} />)
    const healthText = container.querySelector('.text-warning-yellow')
    expect(healthText).toBeInTheDocument()
  })
})
