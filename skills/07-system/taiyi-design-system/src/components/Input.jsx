import React from 'react'
import '../styles.css'

/**
 * 太一输入框组件 - 苹果设计风格
 * 
 * @param {string} type - 输入类型 (text/password/email/number)
 * @param {string} placeholder - 占位符
 * @param {string} value - 输入值
 * @param {function} onChange - 变化事件
 * @param {boolean} disabled - 是否禁用
 * @param {boolean} error - 是否错误状态
 * @param {string} label - 标签
 * @param {string} className - 额外样式类
 */
function Input({ 
  type = 'text', 
  placeholder, 
  value, 
  onChange, 
  disabled = false, 
  error = false,
  label,
  className = ''
}) {
  return (
    <div className={`mb-4 ${className}`}>
      {label && (
        <label className="block text-sm font-medium text-gray-700 mb-2">
          {label}
        </label>
      )}
      <input
        type={type}
        className={`
          w-full px-4 py-2
          border rounded-lg
          focus:outline-none focus:ring-2 focus:ring-[#007AFF] focus:border-transparent
          transition-all duration-200
          ${error 
            ? 'border-red-500 focus:ring-red-500' 
            : 'border-gray-300 hover:border-gray-400'
          }
          ${disabled ? 'bg-gray-100 cursor-not-allowed' : 'bg-white'}
        `}
        placeholder={placeholder}
        value={value}
        onChange={onChange}
        disabled={disabled}
      />
      {error && (
        <p className="mt-1 text-sm text-red-500">
          {error}
        </p>
      )}
    </div>
  )
}

export default Input
