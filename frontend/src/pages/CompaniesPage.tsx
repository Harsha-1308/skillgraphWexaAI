import { useQuery } from '@tanstack/react-query';
import { Link } from 'react-router-dom';
import { Building2, MapPin, ChevronRight } from 'lucide-react';
import { fetchCompanies } from '../services/api';
import LoadingSpinner from '../components/LoadingSpinner';
import ErrorMessage from '../components/ErrorMessage';
import EmptyState from '../components/EmptyState';

export default function CompaniesPage() {
  const { data, isLoading, error } = useQuery({ queryKey: ['companies'], queryFn: fetchCompanies });

  if (isLoading) return <LoadingSpinner message="Loading companies..." />;
  if (error) return <ErrorMessage />;
  if (!data?.length) return <EmptyState icon={Building2} title="No companies found" />;

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white">Companies</h1>
        <p className="text-gray-400 mt-1">{data.length} companies in the graph</p>
      </div>
      <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
        {data.map((co) => (
          <Link key={co.id} to={`/companies/${co.id}`}
            className="group bg-gray-900 border border-gray-800 rounded-xl p-5 hover:border-indigo-700 transition-all"
          >
            <div className="flex items-start justify-between mb-3">
              <div className="w-10 h-10 rounded-xl bg-gray-800 border border-gray-700 flex items-center justify-center text-indigo-400 font-bold">
                {co.name[0]}
              </div>
              <ChevronRight className="w-4 h-4 text-gray-600 group-hover:text-indigo-400" />
            </div>
            <h3 className="font-semibold text-white group-hover:text-indigo-300 mb-0.5">{co.name}</h3>
            <p className="text-xs text-indigo-400/70 mb-2">{co.industry}</p>
            <p className="text-sm text-gray-400 line-clamp-2 mb-3">{co.description}</p>
            <div className="flex items-center gap-1 text-xs text-gray-500">
              <MapPin className="w-3 h-3" />{co.location}
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
}
