interface Props {
  message?: string;
  size?: 'sm' | 'md' | 'lg';
}

export default function LoadingSpinner({ message = 'Loading...', size = 'md' }: Props) {
  const sizeClass = { sm: 'w-4 h-4', md: 'w-8 h-8', lg: 'w-12 h-12' }[size];
  return (
    <div className="flex flex-col items-center justify-center py-12 gap-3 text-gray-400">
      <div className={`${sizeClass} border-2 border-indigo-500/30 border-t-indigo-500 rounded-full animate-spin`} />
      <p className="text-sm">{message}</p>
    </div>
  );
}
