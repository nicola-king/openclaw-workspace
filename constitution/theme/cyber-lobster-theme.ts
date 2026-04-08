/**
 * 🦞 赛博龙虾主题配置
 * 灵感来源：SAYELF 2026-04-02 22:10 发送的机械龙虾图腾
 */

export const CYBER_LOBSTER_THEME = {
  // 主色调 - 蓝紫霓虹
  primary: {
    50: '#F5F3FF',
    100: '#EDE9FE',
    200: '#DDD6FE',
    300: '#C4B5FD',
    400: '#A78BFA',
    500: '#8B5CF6',  // 主色
    600: '#7C3AED',
    700: '#6D28D9',
    800: '#5B21B6',
    900: '#4C1D95',
    950: '#2E1065',
  },
  
  // 强调色 - 龙虾红
  accent: {
    50: '#FEF2F2',
    100: '#FEE2E2',
    200: '#FECACA',
    300: '#FCA5A5',
    400: '#F87171',
    500: '#FF6B6B',  // 强调色
    600: '#EF4444',
    700: '#DC2626',
    800: '#B91C1C',
    900: '#991B1B',
  },
  
  // 背景色 - 深空黑
  background: {
    50: '#F8F8FF',
    100: '#F0F0FA',
    200: '#E0E0F0',
    300: '#C8C8D8',
    400: '#A0A0B8',
    500: '#787890',
    600: '#505068',
    700: '#383850',
    800: '#202038',
    900: '#0D0D1A',  // 深空黑背景
    950: '#05050A',
  },
  
  // 霓虹高光
  neon: {
    blue: '#00F0FF',    // 赛博蓝
    purple: '#9D5BFF',  // 霓虹紫
    pink: '#FF00FF',    // 赛博粉
  },
  
  // 渐变配置
  gradients: {
    // 蓝紫渐变（主渐变）
    primary: 'linear-gradient(135deg, #5A4B9E 0%, #9D5BFF 100%)',
    // 龙虾红渐变
    accent: 'linear-gradient(135deg, #FF6B6B 0%, #FF8E8E 100%)',
    // 赛博霓虹渐变
    cyber: 'linear-gradient(135deg, #00F0FF 0%, #9D5BFF 50%, #FF00FF 100%)',
    // 深空背景渐变
    background: 'linear-gradient(180deg, #0D0D1A 0%, #1A1A2E 100%)',
  },
  
  // 阴影效果
  shadows: {
    // 霓虹光晕
    neonGlow: '0 0 10px rgba(0, 240, 255, 0.5), 0 0 20px rgba(0, 240, 255, 0.3)',
    // 紫色光晕
    purpleGlow: '0 0 10px rgba(157, 91, 255, 0.5), 0 0 20px rgba(157, 91, 255, 0.3)',
    // 龙虾红光晕
    lobsterGlow: '0 0 10px rgba(255, 107, 107, 0.5), 0 0 20px rgba(255, 107, 107, 0.3)',
  },
  
  // 字体颜色
  text: {
    primary: '#FFFFFF',
    secondary: '#C4B5FD',
    muted: '#787890',
    inverse: '#0D0D1A',
  },
  
  // 边框
  border: {
    default: 'rgba(139, 92, 246, 0.3)',
    hover: 'rgba(139, 92, 246, 0.6)',
    active: '#8B5CF6',
  },
};

// CSS 变量导出
export const CSS_VARIABLES = `
:root {
  /* 主色 - 蓝紫霓虹 */
  --primary-50: ${CYBER_LOBSTER_THEME.primary[50]};
  --primary-100: ${CYBER_LOBSTER_THEME.primary[100]};
  --primary-200: ${CYBER_LOBSTER_THEME.primary[200]};
  --primary-300: ${CYBER_LOBSTER_THEME.primary[300]};
  --primary-400: ${CYBER_LOBSTER_THEME.primary[400]};
  --primary-500: ${CYBER_LOBSTER_THEME.primary[500]};
  --primary-600: ${CYBER_LOBSTER_THEME.primary[600]};
  --primary-700: ${CYBER_LOBSTER_THEME.primary[700]};
  --primary-800: ${CYBER_LOBSTER_THEME.primary[800]};
  --primary-900: ${CYBER_LOBSTER_THEME.primary[900]};
  --primary-950: ${CYBER_LOBSTER_THEME.primary[950]};
  
  /* 强调色 - 龙虾红 */
  --accent-50: ${CYBER_LOBSTER_THEME.accent[50]};
  --accent-100: ${CYBER_LOBSTER_THEME.accent[100]};
  --accent-200: ${CYBER_LOBSTER_THEME.accent[200]};
  --accent-300: ${CYBER_LOBSTER_THEME.accent[300]};
  --accent-400: ${CYBER_LOBSTER_THEME.accent[400]};
  --accent-500: ${CYBER_LOBSTER_THEME.accent[500]};
  --accent-600: ${CYBER_LOBSTER_THEME.accent[600]};
  --accent-700: ${CYBER_LOBSTER_THEME.accent[700]};
  --accent-800: ${CYBER_LOBSTER_THEME.accent[800]};
  --accent-900: ${CYBER_LOBSTER_THEME.accent[900]};
  
  /* 背景色 - 深空黑 */
  --background-50: ${CYBER_LOBSTER_THEME.background[50]};
  --background-100: ${CYBER_LOBSTER_THEME.background[100]};
  --background-200: ${CYBER_LOBSTER_THEME.background[200]};
  --background-300: ${CYBER_LOBSTER_THEME.background[300]};
  --background-400: ${CYBER_LOBSTER_THEME.background[400]};
  --background-500: ${CYBER_LOBSTER_THEME.background[500]};
  --background-600: ${CYBER_LOBSTER_THEME.background[600]};
  --background-700: ${CYBER_LOBSTER_THEME.background[700]};
  --background-800: ${CYBER_LOBSTER_THEME.background[800]};
  --background-900: ${CYBER_LOBSTER_THEME.background[900]};
  --background-950: ${CYBER_LOBSTER_THEME.background[950]};
  
  /* 霓虹高光 */
  --neon-blue: ${CYBER_LOBSTER_THEME.neon.blue};
  --neon-purple: ${CYBER_LOBSTER_THEME.neon.purple};
  --neon-pink: ${CYBER_LOBSTER_THEME.neon.pink};
  
  /* 渐变 */
  --gradient-primary: ${CYBER_LOBSTER_THEME.gradients.primary};
  --gradient-accent: ${CYBER_LOBSTER_THEME.gradients.accent};
  --gradient-cyber: ${CYBER_LOBSTER_THEME.gradients.cyber};
  --gradient-background: ${CYBER_LOBSTER_THEME.gradients.background};
  
  /* 阴影 */
  --shadow-neon-glow: ${CYBER_LOBSTER_THEME.shadows.neonGlow};
  --shadow-purple-glow: ${CYBER_LOBSTER_THEME.shadows.purpleGlow};
  --shadow-lobster-glow: ${CYBER_LOBSTER_THEME.shadows.lobsterGlow};
  
  /* 字体颜色 */
  --text-primary: ${CYBER_LOBSTER_THEME.text.primary};
  --text-secondary: ${CYBER_LOBSTER_THEME.text.secondary};
  --text-muted: ${CYBER_LOBSTER_THEME.text.muted};
  --text-inverse: ${CYBER_LOBSTER_THEME.text.inverse};
  
  /* 边框 */
  --border-default: ${CYBER_LOBSTER_THEME.border.default};
  --border-hover: ${CYBER_LOBSTER_THEME.border.hover};
  --border-active: ${CYBER_LOBSTER_THEME.border.active};
}
`;

export default CYBER_LOBSTER_THEME;
