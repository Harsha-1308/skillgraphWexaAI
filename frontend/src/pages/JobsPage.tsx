import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { Link } from 'react-router-dom';
import { Briefcase, MapPin, DollarSign, ChevronRight } from 'lucide-react';
import { fetchJobs } from '../services/api';
import LoadingSpinner from '../components/LoadingSpinner';
import ErrorMessage from '../components/ErrorMessage';
import EmptyState from '../components/EmptyState';

export default function JobsPage() {
  const [search, setSearch] = useState('');
  const { data, isLoading, error } = useQuery({ queryKey: ['jobs'], queryFn: fetchJobs });

  const filtered = data?.filter(
    (j) => j.title.toLowerCase().includes(search.toLowerCase()) ||
            j.company_name.toLowerCase().includes(search.toLowerCase())
  ) ?? [];

  if (isLoading) return <LoadingSpinner message="Loading jobs..." />;
  if (error) return <ErrorMessage />;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white">Jobs</h1>
          <p className="text-gray-400 mt-1">{data?.length ?? 0} open positions</p>
        </div>
      </div>
      <input
        type="search"
        placeholder="Search jobs or companies..."
        value={search}
        onChange={(e) => setSearch(e.target.value)}
        className="w-full bg-gray-900 border border-gray-700 rounded-xl px-4 py-2.5 text-white placeholder-gray-500 focus:outline-none focus:border-indigo-500"
      />
      {filtered.length === 0 ? (
        <EmptyState icon={Briefcase} title="No jobs found" description="Try adjusting your search." />
      ) : (
        <div className="grid sm:grid-cols-2 gap-4">
          {filtered.map((j) => (
            <Link key={j.id} to={`/jobs/${j.id}`}
              className="group bg-gray-900 border border-gray-800 rounded-xl p-5 hover:border-indigo-700 transition-all"
            >
              <div className="flex items-start justify-between gap-2 mb-3">
                <div>
                  <h3 className="font-semibold text-white group-hover:text-indigo-300">{j.title}</h3>
                  <p className="text-sm text-gray-400">{j.company_name}</p>
                </div>
                <ChevronRight className="w-4 h-4 text-gray-600 group-hover:text-indigo-400 mt-1 flex-shrink-0" />
              </div>
              <p className="text-sm text-gray-400 line-clamp-2 mb-3">{j.description}</p>
              <div className="flex flex-wrap gap-3 text-xs text-gray-500">
                <span className="flex items-center gap-1"><MapPin className="w-3 h-3" />{j.location}</span>
                {j.salary_min && (
                  <span className="flex items-center gap-1">
                    <DollarSign className="w-3 h-3" />
                    {(j.salary_min / 1000).toFixed(0)}k–{(j.salary_max! / 1000).toFixed(0)}k
                  </span>
                )}
                <span className="capitalize">{j.employment_type}</span>
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}
