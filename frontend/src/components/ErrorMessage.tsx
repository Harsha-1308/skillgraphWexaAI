import { AlertTriangle } from 'lucide-react';

interface Props {
  title?: string;
  message?: string;
}

export default function ErrorMessage({
  title = 'Something went wrong',
  message = 'Graph database is currently unavailable. Please try again later.',
}: Props) {
  return (
    <div className="flex items-start gap-3 p-4 rounded-xl bg-red-950/40 border border-red-800/50 text-red-300">
      <AlertTriangle className="w-5 h-5 mt-0.5 flex-shrink-0" />
      <div>
        <p className="font-semibold">{title}</p>
        <p className="text-sm text-red-400 mt-0.5">{message}</p>
      </div>
    </div>
  );
}
