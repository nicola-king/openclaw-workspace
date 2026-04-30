import { test, expect } from '@playwright/test'

test.describe('Agents 页面视觉测试', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('http://localhost:3000/agents')
  })

  test('Agents 页面整体布局', async ({ page }) => {
    await expect(page).toHaveScreenshot('agents-full.png', {
      fullPage: true,
      maxDiffPixels: 200
    })
  })

  test('Agent 列表表格', async ({ page }) => {
    const table = page.locator('table')
    await expect(table).toHaveScreenshot('agents-table.png')
  })

  test('搜索和筛选控件', async ({ page }) => {
    const controls = page.locator('input[type="text"], select').first()
    await expect(controls).toBeVisible()
    await expect(page).toHaveScreenshot('agents-controls.png')
  })

  test('统计卡片', async ({ page }) => {
    const stats = page.locator('grid').last()
    await expect(stats).toHaveScreenshot('agents-stats.png')
  })
})
