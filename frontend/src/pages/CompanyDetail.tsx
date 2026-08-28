import { useParams, Link } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { ArrowLeft, Briefcase, MapPin } from 'lucide-react';
import { fetchCompany } from '../services/api';
import LoadingSpinner from '../components/LoadingSpinner';
import ErrorMessage from '../components/ErrorMessage';
import SkillBadge from '../components/SkillBadge';

export default function CompanyDetail() {
  const { id } = useParams<{ id: string }>();
  const { data, isLoading, error } = useQuery({
    queryKey: ['company', id],
    queryFn: () => fetchCompany(id!),
    enabled: !!id,
  });

  if (isLoading) return <LoadingSpinner message="Loading company details..." />;
  if (error) return <ErrorMessage />;
  if (!data) return null;

  return (
    <div className="space-y-6 max-w-4xl">
      <Link to="/companies" className="inline-flex items-center gap-1.5 text-sm text-gray-400 hover:text-white">
        <ArrowLeft className="w-4 h-4" /> Back to companies
      </Link>

      <div className="bg-gray-900 border border-gray-800 rounded-xl p-6">
        <div className="flex items-start gap-4 mb-4">
          <div className="w-14 h-14 rounded-xl bg-gray-800 border border-gray-700 flex items-center justify-center text-indigo-400 font-bold text-2xl flex-shrink-0">
            {data.name[0]}
          </div>
          <div>
            <h1 className="text-2xl font-bold text-white">{data.name}</h1>
            <p className="text-indigo-400">{data.industry}</p>
            <p className="text-sm text-gray-500 mt-0.5 flex items-center gap-1"><MapPin className="w-3 h-3" />{data.location}</p>
          </div>
        </div>
        <p className="text-gray-400">{data.description}</p>

        {data.top_skills.length > 0 && (
          <div className="mt-4">
            <p className="text-xs font-medium text-gray-500 uppercase tracking-wider mb-2">Most Required Skills</p>
            <div className="flex flex-wrap gap-2">
              {data.top_skills.map((s) => (
                <SkillBadge key={s} name={s} />
              ))}
            </div>
          </div>
        )}
      </div>

      <div>
        <h2 className="font-semibold text-white mb-3">Open Positions ({data.total_jobs})</h2>
        <div className="space-y-3">
          {data.jobs.map((job) => (
            <Link key={job.id} to={`/jobs/${job.id}`}
              className="flex items-center gap-4 p-4 bg-gray-900 border border-gray-800 rounded-xl hover:border-indigo-700 transition-all group"
            >
              <Briefcase className="w-5 h-5 text-gray-600 flex-shrink-0" />
              <div className="flex-1 min-w-0">
                <p className="font-medium text-white group-hover:text-indigo-300">{job.title}</p>
                <p className="text-sm text-gray-500">{job.experience_required}+ years · {job.employment_type}</p>
                <div className="flex flex-wrap gap-1 mt-2">
                  {job.required_skills.slice(0, 5).map((s) => (
                    <SkillBadge key={s} name={s} size="sm" />
                  ))}
                  {job.required_skills.length > 5 && (
                    <span className="text-xs text-gray-500">+{job.required_skills.length - 5} more</span>
                  )}
                </div>
              </div>
            </Link>
          ))}
        </div>
      </div>
    </div>
  );
}
