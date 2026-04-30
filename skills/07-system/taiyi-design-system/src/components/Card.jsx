import React from 'react'
import '../styles.css'

/**
 * 太一卡片组件 - 苹果设计风格
 * 
 * @param {string} title - 卡片标题
 * @param {string} variant - 卡片变体 (default/elevated/bordered)
 * @param {boolean} hoverable - 是否可悬浮
 * @param {string} children - 卡片内容
 * @param {function} onClick - 点击事件
 */
function Card({ 
  title, 
  variant = 'default', 
  hoverable = false,
  children, 
  onClick,
  className = ''
}) {
  // 变体样式
  const variantStyles = {
    default: 'bg-white shadow-md',
    elevated: 'bg-white shadow-lg',
    bordered: 'bg-white border border-gray-200',
    zen: 'bg-[#F8F9FA] border-l-4 border-[#7D8447]',
    skyblue: 'bg-[#F0F9FF] border-l-4 border-[#87CEEB]',
  }
  
  return (
    <div
      className={`
        ${variantStyles[variant]}
        rounded-xl p-6
        ${hoverable ? 'hover:shadow-lg transition-shadow cursor-pointer' : ''}
        ${className}
      `}
      onClick={onClick}
    >
      {title && (
        <h3 className="text-xl font-bold text-gray-800 mb-4">
          {title}
        </h3>
      )}
      <div className="text-gray-600">
        {children}
      </div>
    </div>
  )
}

export default Card
