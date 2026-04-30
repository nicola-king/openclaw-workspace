/**
 * 太一 AGI 设计系统
 * 
 * 融合原则：苹果 80% + 东方 15% + 中国 5%
 * 
 * @module @taiyi/design-system
 */

// 样式
import './styles.css'

// 组件
export { default as Button } from './components/Button'
export { default as Card } from './components/Card'
export { default as Input } from './components/Input'

// 设计令牌
export const designTokens = {
  colors: {
    primary: '#8E8E93',
    accent: '#007AFF',
    success: '#34C759',
    warning: '#FF9500',
    error: '#FF3B30',
    
    // 东方色彩
    zen: '#7D8447',
    sakura: '#FFB7C5',
    
    // 中国色彩
    skyblue: '#87CEEB',
    cinnabar: '#E60000',
    ink: '#2C2C2C',
  },
  
  spacing: {
    1: '4px',
    2: '8px',
    3: '16px',
    4: '24px',
    5: '32px',
    6: '48px',
  },
  
  radius: {
    sm: '8px',
    md: '12px',
    lg: '20px',
    xl: '32px',
    full: '9999px',
  },
  
  shadows: {
    sm: '0 1px 2px rgba(0,0,0,0.05)',
    md: '0 4px 8px rgba(0,0,0,0.1)',
    lg: '0 8px 16px rgba(0,0,0,0.15)',
    xl: '0 16px 32px rgba(0,0,0,0.2)',
  },
}

// 版本
export const version = '1.0.0'

// 默认导出
export default {
  Button: () => import('./components/Button'),
  Card: () => import('./components/Card'),
  Input: () => import('./components/Input'),
  designTokens,
  version,
}
