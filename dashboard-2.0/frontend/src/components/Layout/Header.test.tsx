import { render, screen } from '@testing-library/react'
import { describe, it, expect } from 'vitest'
import Header from './Header'

describe('Header', () => {
  it('渲染 Logo', () => {
    render(<Header />)
    expect(screen.getByText('太一 Dashboard 2.0')).toBeInTheDocument()
  })

  it('渲染导航链接', () => {
    render(<Header />)
    expect(screen.getByText('仪表盘')).toBeInTheDocument()
    expect(screen.getByText('Agent')).toBeInTheDocument()
    expect(screen.getByText('Skill')).toBeInTheDocument()
  })

  it('显示系统状态', () => {
    render(<Header />)
    expect(screen.getByText('系统正常')).toBeInTheDocument()
  })

  it('显示版本号', () => {
    render(<Header />)
    expect(screen.getByText('v2.0.0')).toBeInTheDocument()
  })
})
