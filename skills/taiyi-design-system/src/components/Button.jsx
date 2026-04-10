import React from 'react'
import '../styles.css'

/**
 * 太一按钮组件 - 苹果设计风格
 * 
 * @param {string} variant - 按钮变体 (primary/secondary/danger/ghost)
 * @param {string} size - 按钮大小 (sm/md/lg)
 * @param {boolean} disabled - 是否禁用
 * @param {boolean} loading - 是否加载中
 * @param {string} children - 按钮内容
 * @param {function} onClick - 点击事件
 */
function Button({ 
  variant = 'primary', 
  size = 'md', 
  disabled = false, 
  loading = false,
  children, 
  onClick,
  className = ''
}) {
  // 变体样式
  const variantStyles = {
    primary: 'bg-[#007AFF] text-white hover:bg-[#0056CC]',
    secondary: 'bg-gray-100 text-gray-800 hover:bg-gray-200',
    danger: 'bg-red-500 text-white hover:bg-red-600',
    ghost: 'bg-transparent text-[#007AFF] hover:bg-gray-50',
    zen: 'bg-[#7D8447] text-white hover:bg-[#6A703D]',
    skyblue: 'bg-[#87CEEB] text-white hover:bg-[#6BB6E8]',
  }
  
  // 大小样式
  const sizeStyles = {
    sm: 'px-3 py-1.5 text-xs',
    md: 'px-6 py-3 text-sm',
    lg: 'px-8 py-4 text-base',
  }
  
  return (
    <button
      className={`
        ${variantStyles[variant]}
        ${sizeStyles[size]}
        rounded-lg font-medium
        transition-all duration-200 ease-out
        focus:outline-none focus:ring-2 focus:ring-[#007AFF] focus:ring-offset-2
        disabled:opacity-50 disabled:cursor-not-allowed
        ${loading ? 'opacity-70 cursor-wait' : ''}
        ${className}
      `}
      disabled={disabled || loading}
      onClick={onClick}
    >
      {loading ? (
        <span className="flex items-center justify-center">
          <svg className="animate-spin -ml-1 mr-2 h-4 w-4" fill="none" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
          </svg>
          加载中...
        </span>
      ) : children}
    </button>
  )
}

export default Button
