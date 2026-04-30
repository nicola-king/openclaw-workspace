import { render, screen } from '@testing-library/react'
import { describe, it, expect } from 'vitest'
import Timeline from './Timeline'

const mockEvents = [
  { time: '23:05', event: 'Dashboard 2.0 设计完成', type: 'success' as const },
  { time: '22:52', event: '任务成果汇报完成', type: 'success' as const },
  { time: '22:44', event: '进度汇报完成', type: 'info' as const },
]

describe('Timeline', () => {
  it('渲染事件列表', () => {
    render(<Timeline events={mockEvents} />)
    expect(screen.getByText('Dashboard 2.0 设计完成')).toBeInTheDocument()
    expect(screen.getByText('任务成果汇报完成')).toBeInTheDocument()
  })

  it('显示时间戳', () => {
    render(<Timeline events={mockEvents} />)
    expect(screen.getByText('23:05')).toBeInTheDocument()
    expect(screen.getByText('22:52')).toBeInTheDocument()
  })

  it('渲染正确数量的事件', () => {
    const { container } = render(<Timeline events={mockEvents} />)
    const eventItems = container.querySelectorAll('[data-testid="timeline-event"]')
    expect(eventItems).toHaveLength(3)
  })
})
