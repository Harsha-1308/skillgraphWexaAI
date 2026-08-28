import { useParams, Link } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { ArrowLeft, MapPin, DollarSign, Clock } from 'lucide-react';
import { fetchJob } from '../services/api';
import LoadingSpinner from '../components/LoadingSpinner';
import ErrorMessage from '../components/ErrorMessage';
import SkillBadge from '../components/SkillBadge';

const importanceColor: Record<string, string> = {
  critical: 'text-red-400',
  high: 'text-amber-400',
  medium: 'text-blue-400',
  low: 'text-gray-400',
};

export default function JobDetail() {
  const { id } = useParams<{ id: string }>();
  const { data, isLoading, error } = useQuery({
    queryKey: ['job', id],
    queryFn: () => fetchJob(id!),
    enabled: !!id,
  });

  if (isLoading) return <LoadingSpinner message="Loading job details..." />;
  if (error) return <ErrorMessage />;
  if (!data) return null;

  return (
    <div className="space-y-6 max-w-3xl">
      <Link to="/jobs" className="inline-flex items-center gap-1.5 text-sm text-gray-400 hover:text-white">
        <ArrowLeft className="w-4 h-4" /> Back to jobs
      </Link>

      <div className="bg-gray-900 border border-gray-800 rounded-xl p-6 space-y-4">
        <div>
          <h1 className="text-2xl font-bold text-white">{data.title}</h1>
          <Link to={`/companies/${data.company_id}`} className="text-indigo-400 hover:text-indigo-300 font-medium">
            {data.company_name}
          </Link>
          {data.role_name && <span className="ml-2 text-gray-500 text-sm">· {data.role_name}</span>}
        </div>

        <div className="flex flex-wrap gap-4 text-sm text-gray-400">
          <span className="flex items-center gap-1.5"><MapPin className="w-4 h-4" />{data.location}</span>
          <span className="flex items-center gap-1.5"><Clock className="w-4 h-4" />{data.experience_required}+ years</span>
          {data.salary_min && (
            <span className="flex items-center gap-1.5">
              <DollarSign className="w-4 h-4" />
              ${(data.salary_min / 1000).toFixed(0)}k – ${(data.salary_max! / 1000).toFixed(0)}k
            </span>
          )}
          <span className="capitalize bg-gray-800 rounded-full px-2.5 py-0.5">{data.employment_type}</span>
        </div>

        <div>
          <h2 className="font-semibold text-white mb-2">About this role</h2>
          <p className="text-gray-400 text-sm leading-relaxed">{data.description}</p>
        </div>

        {data.required_skills.length > 0 && (
          <div>
            <h2 className="font-semibold text-white mb-3">Required Skills</h2>
            <div className="space-y-2">
              {data.required_skills.map((s) => (
                <div key={s.id} className="flex items-center justify-between p-3 bg-gray-800 rounded-lg">
                  <div className="flex items-center gap-2">
                    <SkillBadge name={s.name} category={s.category} />
                    <span className="text-xs text-gray-500">min. {s.minimum_level}</span>
                  </div>
                  <span className={`text-xs font-medium capitalize ${importanceColor[s.importance] ?? 'text-gray-400'}`}>
                    {s.importance}
                  </span>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
