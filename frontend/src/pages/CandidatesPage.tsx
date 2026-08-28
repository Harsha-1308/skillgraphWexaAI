import { useQuery } from '@tanstack/react-query';
import { Link } from 'react-router-dom';
import { Users, MapPin, Clock, ChevronRight } from 'lucide-react';
import { fetchCandidates } from '../services/api';
import LoadingSpinner from '../components/LoadingSpinner';
import ErrorMessage from '../components/ErrorMessage';
import EmptyState from '../components/EmptyState';

export default function CandidatesPage() {
  const { data, isLoading, error } = useQuery({ queryKey: ['candidates'], queryFn: fetchCandidates });

  if (isLoading) return <LoadingSpinner message="Loading candidates..." />;
  if (error) return <ErrorMessage />;
  if (!data?.length) return <EmptyState icon={Users} title="No candidates found" description="Seed the database to see candidates." />;

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white">Candidates</h1>
        <p className="text-gray-400 mt-1">{data.length} candidates in the graph</p>
      </div>
      <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
        {data.map((c) => (
          <Link key={c.id} to={`/candidates/${c.id}`}
            className="group bg-gray-900 border border-gray-800 rounded-xl p-5 hover:border-indigo-700 transition-all"
          >
            <div className="flex items-start gap-3 mb-3">
              <div className="w-11 h-11 rounded-full bg-indigo-900/60 border border-indigo-700/50 flex items-center justify-center text-indigo-300 font-bold text-lg flex-shrink-0">
                {c.name[0]}
              </div>
              <div className="min-w-0">
                <h3 className="font-semibold text-white group-hover:text-indigo-300 truncate">{c.name}</h3>
                <p className="text-xs text-gray-500 truncate">{c.email}</p>
              </div>
            </div>
            <p className="text-sm text-gray-400 line-clamp-2 mb-3">{c.bio}</p>
            <div className="flex items-center gap-4 text-xs text-gray-500">
              <span className="flex items-center gap-1"><Clock className="w-3 h-3" />{c.experience_years}y exp</span>
              <span className="flex items-center gap-1 truncate"><MapPin className="w-3 h-3" />{c.location}</span>
            </div>
            <div className="flex items-center justify-end mt-3">
              <ChevronRight className="w-4 h-4 text-gray-600 group-hover:text-indigo-400 transition-colors" />
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
}
