// src/components/ui/button.tsx
import React from 'react'
import { cn } from '@/lib/utils'

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'default' | 'outline' | 'secondary' | 'ghost'
}

const variantStyles = {
  default: 'bg-black text-white hover:bg-neutral-800',
  outline:
    'border border-gray-300 bg-transparent text-gray-700 hover:bg-gray-100',
  secondary:
    'bg-gray-200 text-gray-800 hover:bg-gray-300',
  ghost: 'bg-transparent text-gray-600 hover:text-gray-900 hover:bg-gray-100',
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant = 'default', ...props }, ref) => {
    return (
      <button
        ref={ref}
        className={cn(
          'inline-flex items-center justify-center rounded-xl px-4 py-2 text-sm font-medium transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2',
          variantStyles[variant],
          className
        )}
        {...props}
      />
    )
  }
)

Button.displayName = 'Button'

export { Button }