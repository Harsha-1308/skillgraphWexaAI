interface Props {
  name: string;
  category?: string;
  level?: string;
  size?: 'sm' | 'md';
  variant?: 'default' | 'matched' | 'missing' | 'related';
}

const categoryColors: Record<string, string> = {
  'Programming': 'bg-blue-900/40 text-blue-300 border-blue-700/50',
  'Frontend': 'bg-purple-900/40 text-purple-300 border-purple-700/50',
  'Backend': 'bg-cyan-900/40 text-cyan-300 border-cyan-700/50',
  'AI/ML': 'bg-orange-900/40 text-orange-300 border-orange-700/50',
  'DevOps': 'bg-green-900/40 text-green-300 border-green-700/50',
  'Cloud': 'bg-sky-900/40 text-sky-300 border-sky-700/50',
  'Database': 'bg-yellow-900/40 text-yellow-300 border-yellow-700/50',
  'Data Engineering': 'bg-pink-900/40 text-pink-300 border-pink-700/50',
  'Tools': 'bg-gray-700/60 text-gray-300 border-gray-600',
  'Architecture': 'bg-red-900/40 text-red-300 border-red-700/50',
  'CS Fundamentals': 'bg-teal-900/40 text-teal-300 border-teal-700/50',
};

const variantClasses: Record<string, string> = {
  matched: 'bg-emerald-900/40 text-emerald-300 border-emerald-700/50',
  missing: 'bg-red-900/40 text-red-300 border-red-700/50',
  related: 'bg-violet-900/40 text-violet-300 border-violet-700/50',
  default: '',
};

export default function SkillBadge({ name, category, variant = 'default', size = 'sm' }: Props) {
  const colorClass = variant !== 'default'
    ? variantClasses[variant]
    : category
    ? (categoryColors[category] ?? 'bg-gray-800 text-gray-300 border-gray-700')
    : 'bg-gray-800 text-gray-300 border-gray-700';

  return (
    <span
      className={`inline-flex items-center border rounded-full font-medium ${
        size === 'sm' ? 'px-2.5 py-0.5 text-xs' : 'px-3 py-1 text-sm'
      } ${colorClass}`}
    >
      {name}
    </span>
  );
}
