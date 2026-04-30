import { test, expect } from '@playwright/test'

test.describe('视觉回归测试', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('http://localhost:3000')
  })

  test('Dashboard 页面整体布局', async ({ page }) => {
    await expect(page).toHaveScreenshot('dashboard-full.png', {
      fullPage: true,
      maxDiffPixels: 200
    })
  })

  test('Dashboard 统计卡片', async ({ page }) => {
    const statsGrid = page.locator('grid').first()
    await expect(statsGrid).toHaveScreenshot('dashboard-stats.png')
  })

  test('Agent 状态卡片', async ({ page }) => {
    const agentCards = page.locator('[data-testid="agent-card"]')
    await expect(agentCards.first()).toHaveScreenshot('agent-card-sample.png')
  })

  test('自进化进度组件', async ({ page }) => {
    const evolutionProgress = page.getByText('自进化程度')
    await expect(evolutionProgress).toBeVisible()
    await expect(page).toHaveScreenshot('evolution-progress.png')
  })

  test('实时任务流图表', async ({ page }) => {
    const chart = page.locator('.recharts-wrapper')
    await expect(chart).toBeVisible()
    await expect(page).toHaveScreenshot('realtime-chart.png')
  })

  test('事件时间线', async ({ page }) => {
    const timeline = page.getByText('事件时间线')
    await expect(timeline).toBeVisible()
    await expect(page).toHaveScreenshot('timeline.png')
  })

  test('Header 导航栏', async ({ page }) => {
    const header = page.locator('header')
    await expect(header).toHaveScreenshot('header.png')
  })

  test('Sidebar 侧边栏', async ({ page }) => {
    const sidebar = page.locator('aside')
    await expect(sidebar).toHaveScreenshot('sidebar.png')
  })

  test('Footer 状态栏', async ({ page }) => {
    const footer = page.locator('footer')
    await expect(footer).toHaveScreenshot('footer.png')
  })
})
