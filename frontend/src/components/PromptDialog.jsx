import { useState } from 'react';
import { X } from 'lucide-react';

/**
 * PromptDialog Component
 * A reusable prompt dialog to replace window.prompt()
 * 
 * Usage:
 * const [showPrompt, setShowPrompt] = useState(false);
 * 
 * <PromptDialog
 *   isOpen={showPrompt}
 *   title="Enter Reason"
 *   message="Please provide a reason:"
 *   placeholder="Enter reason here..."
 *   onConfirm={(value) => { doSomething(value); setShowPrompt(false); }}
 *   onCancel={() => setShowPrompt(false)}
 * />
 */
export default function PromptDialog({ 
  isOpen, 
  title = "Input Required", 
  message, 
  placeholder = "Enter value...",
  defaultValue = "",
  confirmText = "Submit",
  cancelText = "Cancel",
  onConfirm, 
  onCancel 
}) {
  const [value, setValue] = useState(defaultValue);

  if (!isOpen) return null;

  const handleConfirm = () => {
    if (value.trim()) {
      onConfirm(value);
      setValue(defaultValue);
    }
  };

  const handleCancel = () => {
    setValue(defaultValue);
    onCancel();
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleConfirm();
    } else if (e.key === 'Escape') {
      handleCancel();
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50 backdrop-blur-sm">
      <div className="bg-slate-800 rounded-2xl shadow-2xl max-w-md w-full border border-slate-700 animate-in fade-in zoom-in duration-200">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-slate-700">
          <h3 className="text-xl font-bold text-white">{title}</h3>
          <button
            onClick={handleCancel}
            className="text-slate-400 hover:text-white transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Body */}
        <div className="p-6 space-y-4">
          {message && <p className="text-slate-300 text-base">{message}</p>}
          
          <input
            type="text"
            value={value}
            onChange={(e) => setValue(e.target.value)}
            onKeyDown={handleKeyPress}
            placeholder={placeholder}
            autoFocus
            className="w-full px-4 py-3 bg-slate-900 border border-slate-600 rounded-lg text-white placeholder-slate-400 focus:outline-none focus:border-cyan-500 focus:ring-2 focus:ring-cyan-500/20 transition-all"
          />
        </div>

        {/* Footer */}
        <div className="flex items-center justify-end gap-3 p-6 border-t border-slate-700">
          <button
            onClick={handleCancel}
            className="px-6 py-2.5 rounded-lg bg-slate-700 hover:bg-slate-600 text-white font-medium transition-all duration-200"
          >
            {cancelText}
          </button>
          <button
            onClick={handleConfirm}
            disabled={!value.trim()}
            className="px-6 py-2.5 rounded-lg bg-gradient-to-r from-cyan-500 to-teal-500 hover:from-cyan-600 hover:to-teal-600 text-white font-medium transition-all duration-200 shadow-lg disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {confirmText}
          </button>
        </div>
      </div>
    </div>
  );
}
