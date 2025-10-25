import { useState } from 'react';
import { Plus, Edit2, Trash2, Eye, TrendingUp, Zap, Trophy, X } from 'lucide-react';

const programs = [
  {
    id: 1,
    name: 'Two Phase $100K',
    type: 'two_phase',
    accountSize: 100000,
    profitSplit: 80,
    phase1Target: 8,
    phase2Target: 5,
    maxDailyLoss: 5,
    maxTotalLoss: 10,
    price: 299,
    enrolledTraders: 234,
    status: 'active',
  },
  {
    id: 2,
    name: 'One Phase $50K',
    type: 'one_phase',
    accountSize: 50000,
    profitSplit: 75,
    phase1Target: 10,
    maxDailyLoss: 5,
    maxTotalLoss: 10,
    price: 199,
    enrolledTraders: 189,
    status: 'active',
  },
  {
    id: 3,
    name: 'Instant Funding $200K',
    type: 'instant',
    accountSize: 200000,
    profitSplit: 90,
    maxDailyLoss: 3,
    maxTotalLoss: 6,
    price: 499,
    enrolledTraders: 67,
    status: 'active',
  },
];

const programTypeConfig = {
  two_phase: {
    label: 'Two Phase',
    gradient: 'from-cyan-400 to-pink-300',
    bgColor: 'bg-gradient-to-br from-cyan-400 to-pink-300',
    color: 'text-indigo-600',
    icon: TrendingUp,
  },
  one_phase: {
    label: 'One Phase',
    gradient: 'from-blue-400 to-cyan-400',
    bgColor: 'bg-gradient-to-br from-blue-400 to-cyan-400',
    color: 'text-blue-600',
    icon: Zap,
  },
  instant: {
    label: 'Instant Funding',
    gradient: 'from-pink-400 to-yellow-300',
    bgColor: 'bg-gradient-to-br from-pink-400 to-yellow-300',
    color: 'text-pink-600',
    icon: Trophy,
  },
};

export default function ProgramsManagement() {
  const [openDialog, setOpenDialog] = useState(false);
  const [selectedProgram, setSelectedProgram] = useState(null);
  const [formData, setFormData] = useState({
    name: '',
    type: 'two_phase',
    accountSize: 100000,
    profitSplit: 80,
    price: 299,
  });

  const handleOpenDialog = (program = null) => {
    if (program) {
      setSelectedProgram(program);
      setFormData(program);
    } else {
      setSelectedProgram(null);
      setFormData({
        name: '',
        type: 'two_phase',
        accountSize: 100000,
        profitSplit: 80,
        price: 299,
      });
    }
    setOpenDialog(true);
  };

  const handleCloseDialog = () => {
    setOpenDialog(false);
    setSelectedProgram(null);
  };

  const handleSave = () => {
    // TODO: Implement save functionality
    handleCloseDialog();
  };

  const handleDelete = (program) => {
    if (window.confirm(`Are you sure you want to delete ${program.name}?`)) {
      // TODO: Implement delete functionality
    }
  };

  return (
    <div>
      {/* Header */}
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Programs Management</h1>
          <p className="mt-2 text-gray-600">Create and manage trading programs</p>
        </div>
        <button
          onClick={() => handleOpenDialog()}
          className="bg-gradient-to-r from-green-400 to-cyan-400 hover:from-cyan-400 hover:to-green-400 text-white px-6 py-3 rounded-lg font-medium transition-all duration-200 flex items-center gap-2 shadow-lg hover:shadow-xl"
        >
          <Plus className="w-5 h-5" />
          Add Program
        </button>
      </div>

      {/* Programs Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {programs.map((program) => {
          const config = programTypeConfig[program.type];
          const Icon = config.icon;

          return (
            <div
              key={program.id}
              className="bg-white rounded-lg shadow-md hover:shadow-xl transition-all duration-300 hover:-translate-y-2 flex flex-col"
            >
              {/* Card Header */}
              <div className={`${config.bgColor} p-6 rounded-t-lg flex items-center gap-4`}>
                <div className="w-14 h-14 bg-white/20 rounded-lg flex items-center justify-center">
                  <Icon className="w-8 h-8 text-white" />
                </div>
                <div className="flex-1">
                  <span className="inline-block px-3 py-1 bg-white/30 text-white text-xs font-semibold rounded-full mb-2">
                    {config.label}
                  </span>
                  <h3 className="text-xl font-bold text-white">{program.name}</h3>
                </div>
              </div>

              {/* Card Content */}
              <div className="p-6 flex-1">
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <p className="text-sm text-gray-500">Account Size</p>
                    <p className="text-xl font-semibold text-gray-900">
                      ${(program.accountSize / 1000).toFixed(0)}K
                    </p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-500">Profit Split</p>
                    <p className="text-xl font-semibold text-green-600">
                      {program.profitSplit}%
                    </p>
                  </div>
                  {program.phase1Target && (
                    <div>
                      <p className="text-sm text-gray-500">Phase 1 Target</p>
                      <p className="text-lg font-semibold text-gray-900">
                        {program.phase1Target}%
                      </p>
                    </div>
                  )}
                  {program.phase2Target && (
                    <div>
                      <p className="text-sm text-gray-500">Phase 2 Target</p>
                      <p className="text-lg font-semibold text-gray-900">
                        {program.phase2Target}%
                      </p>
                    </div>
                  )}
                  <div>
                    <p className="text-sm text-gray-500">Max Daily Loss</p>
                    <p className="text-lg font-semibold text-red-600">
                      {program.maxDailyLoss}%
                    </p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-500">Max Total Loss</p>
                    <p className="text-lg font-semibold text-red-600">
                      {program.maxTotalLoss}%
                    </p>
                  </div>
                </div>

                {/* Price and Enrolled Box */}
                <div className="mt-6 p-4 bg-gray-50 rounded-lg flex justify-between items-center">
                  <div>
                    <p className="text-sm text-gray-500">Price</p>
                    <p className={`text-2xl font-bold ${config.color}`}>
                      ${program.price}
                    </p>
                  </div>
                  <div className="text-right">
                    <p className="text-sm text-gray-500">Enrolled</p>
                    <p className="text-xl font-semibold text-gray-900">
                      {program.enrolledTraders}
                    </p>
                  </div>
                </div>
              </div>

              {/* Card Actions */}
              <div className="px-6 pb-6 flex gap-2">
                <button className="flex-1 px-4 py-2 text-gray-700 hover:bg-gray-100 rounded-lg transition-colors duration-200 flex items-center justify-center gap-2">
                  <Eye className="w-4 h-4" />
                  View
                </button>
                <button
                  onClick={() => handleOpenDialog(program)}
                  className="flex-1 px-4 py-2 text-blue-600 hover:bg-blue-50 rounded-lg transition-colors duration-200 flex items-center justify-center gap-2"
                >
                  <Edit2 className="w-4 h-4" />
                  Edit
                </button>
                <button
                  onClick={() => handleDelete(program)}
                  className="flex-1 px-4 py-2 text-red-600 hover:bg-red-50 rounded-lg transition-colors duration-200 flex items-center justify-center gap-2"
                >
                  <Trash2 className="w-4 h-4" />
                  Delete
                </button>
              </div>
            </div>
          );
        })}
      </div>

      {/* Add/Edit Program Dialog */}
      {openDialog && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-lg shadow-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
            {/* Dialog Header */}
            <div className="flex justify-between items-center p-6 border-b">
              <h2 className="text-2xl font-bold text-gray-900">
                {selectedProgram ? 'Edit Program' : 'Add New Program'}
              </h2>
              <button
                onClick={handleCloseDialog}
                className="text-gray-400 hover:text-gray-600 transition-colors"
              >
                <X className="w-6 h-6" />
              </button>
            </div>

            {/* Dialog Content */}
            <div className="p-6 space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Program Name
                </label>
                <input
                  type="text"
                  value={formData.name}
                  onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="e.g., Two Phase $100K"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Type
                </label>
                <select
                  value={formData.type}
                  onChange={(e) => setFormData({ ...formData, type: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  <option value="two_phase">Two Phase</option>
                  <option value="one_phase">One Phase</option>
                  <option value="instant">Instant Funding</option>
                </select>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Account Size
                  </label>
                  <div className="relative">
                    <span className="absolute left-3 top-2.5 text-gray-500">$</span>
                    <input
                      type="number"
                      value={formData.accountSize}
                      onChange={(e) => setFormData({ ...formData, accountSize: parseInt(e.target.value) })}
                      className="w-full pl-8 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Profit Split
                  </label>
                  <div className="relative">
                    <input
                      type="number"
                      value={formData.profitSplit}
                      onChange={(e) => setFormData({ ...formData, profitSplit: parseInt(e.target.value) })}
                      className="w-full pr-8 pl-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    />
                    <span className="absolute right-3 top-2.5 text-gray-500">%</span>
                  </div>
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Price
                </label>
                <div className="relative">
                  <span className="absolute left-3 top-2.5 text-gray-500">$</span>
                  <input
                    type="number"
                    value={formData.price}
                    onChange={(e) => setFormData({ ...formData, price: parseInt(e.target.value) })}
                    className="w-full pl-8 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                </div>
              </div>
            </div>

            {/* Dialog Actions */}
            <div className="flex justify-end gap-3 p-6 border-t">
              <button
                onClick={handleCloseDialog}
                className="px-6 py-2 text-gray-700 hover:bg-gray-100 rounded-lg transition-colors duration-200"
              >
                Cancel
              </button>
              <button
                onClick={handleSave}
                className="px-6 py-2 bg-gradient-to-r from-green-400 to-cyan-400 hover:from-cyan-400 hover:to-green-400 text-white rounded-lg font-medium transition-all duration-200 shadow-lg"
              >
                {selectedProgram ? 'Save Changes' : 'Create Program'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

