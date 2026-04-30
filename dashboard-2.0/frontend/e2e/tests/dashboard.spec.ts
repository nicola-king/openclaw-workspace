import { test, expect } from '@playwright/test'

test.describe('Dashboard', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('http://localhost:3000')
  })

  test('加载仪表盘页面', async ({ page }) => {
    await expect(page).toHaveTitle('太一 Dashboard 2.0')
  })

  test('显示统计卡片', async ({ page }) => {
    await expect(page.getByText('Agent 数量')).toBeVisible()
    await expect(page.getByText('Skill 数量')).toBeVisible()
    await expect(page.getByText('今日任务')).toBeVisible()
    await expect(page.getByText('系统健康度')).toBeVisible()
  })

  test('显示 Agent 状态', async ({ page }) => {
    await expect(page.getByText('太一')).toBeVisible()
    await expect(page.getByText('知几')).toBeVisible()
    await expect(page.getByText('山木')).toBeVisible()
  })

  test('显示自进化进度', async ({ page }) => {
    await expect(page.getByText('Level 3')).toBeVisible()
    await expect(page.getByText('92%')).toBeVisible()
  })

  test('导航到 Agent 页面', async ({ page }) => {
    await page.getByText('Agent').click()
    await expect(page).toHaveURL('http://localhost:3000/agents')
  })

  test('导航到 Skill 页面', async ({ page }) => {
    await page.getByText('Skill').click()
    await expect(page).toHaveURL('http://localhost:3000/skills')
  })
})
