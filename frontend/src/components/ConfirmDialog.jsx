import { X } from 'lucide-react';

/**
 * ConfirmDialog Component
 * A reusable confirmation dialog to replace window.confirm()
 * 
 * Usage:
 * const [showConfirm, setShowConfirm] = useState(false);
 * 
 * <ConfirmDialog
 *   isOpen={showConfirm}
 *   title="Confirm Action"
 *   message="Are you sure you want to proceed?"
 *   onConfirm={() => { doSomething(); setShowConfirm(false); }}
 *   onCancel={() => setShowConfirm(false)}
 * />
 */
export default function ConfirmDialog({ 
  isOpen, 
  title = "Confirm", 
  message, 
  confirmText = "Confirm",
  cancelText = "Cancel",
  confirmColor = "red", // red, green, blue
  onConfirm, 
  onCancel 
}) {
  if (!isOpen) return null;

  const colorClasses = {
    red: 'bg-gradient-to-r from-red-500 to-red-600 hover:from-red-600 hover:to-red-700',
    green: 'bg-gradient-to-r from-green-500 to-green-600 hover:from-green-600 hover:to-green-700',
    blue: 'bg-gradient-to-r from-blue-500 to-blue-600 hover:from-blue-600 hover:to-blue-700',
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50 backdrop-blur-sm">
      <div className="bg-slate-800 rounded-2xl shadow-2xl max-w-md w-full border border-slate-700 animate-in fade-in zoom-in duration-200">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-slate-700">
          <h3 className="text-xl font-bold text-white">{title}</h3>
          <button
            onClick={onCancel}
            className="text-slate-400 hover:text-white transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Body */}
        <div className="p-6">
          <p className="text-slate-300 text-base leading-relaxed">{message}</p>
        </div>

        {/* Footer */}
        <div className="flex items-center justify-end gap-3 p-6 border-t border-slate-700">
          <button
            onClick={onCancel}
            className="px-6 py-2.5 rounded-lg bg-slate-700 hover:bg-slate-600 text-white font-medium transition-all duration-200"
          >
            {cancelText}
          </button>
          <button
            onClick={onConfirm}
            className={`px-6 py-2.5 rounded-lg text-white font-medium transition-all duration-200 shadow-lg ${colorClasses[confirmColor]}`}
          >
            {confirmText}
          </button>
        </div>
      </div>
    </div>
  );
}
