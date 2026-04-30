import { test, expect } from '@playwright/test'

test.describe('Approvals 页面视觉测试', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('http://localhost:3000/approvals')
  })

  test('Approvals 页面整体布局', async ({ page }) => {
    await expect(page).toHaveScreenshot('approvals-full.png', {
      fullPage: true,
      maxDiffPixels: 200
    })
  })

  test('审批统计卡片', async ({ page }) => {
    const stats = page.locator('grid').first()
    await expect(stats).toHaveScreenshot('approvals-stats.png')
  })

  test('审批列表表格', async ({ page }) => {
    const table = page.locator('table')
    await expect(table).toHaveScreenshot('approvals-table.png')
  })

  test('审批状态标识', async ({ page }) => {
    const statusIcons = page.locator('svg')
    await expect(statusIcons).not.toHaveLength(0)
    await expect(page).toHaveScreenshot('approvals-status.png')
  })
})
