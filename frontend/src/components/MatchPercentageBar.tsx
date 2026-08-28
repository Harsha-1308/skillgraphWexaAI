interface Props {
  percentage: number;
  showLabel?: boolean;
}

function getColor(pct: number) {
  if (pct >= 80) return 'bg-emerald-500';
  if (pct >= 60) return 'bg-indigo-500';
  if (pct >= 40) return 'bg-amber-500';
  return 'bg-red-500';
}

export default function MatchPercentageBar({ percentage, showLabel = true }: Props) {
  const color = getColor(percentage);
  return (
    <div className="flex items-center gap-2">
      <div className="flex-1 h-2 bg-gray-800 rounded-full overflow-hidden">
        <div
          className={`h-full ${color} transition-all duration-500`}
          style={{ width: `${Math.min(percentage, 100)}%` }}
        />
      </div>
      {showLabel && (
        <span className={`text-sm font-bold w-10 text-right ${
          percentage >= 80 ? 'text-emerald-400'
          : percentage >= 60 ? 'text-indigo-400'
          : percentage >= 40 ? 'text-amber-400'
          : 'text-red-400'
        }`}>
          {Math.round(percentage)}%
        </span>
      )}
    </div>
  );
}
