import { useQuery } from '@tanstack/react-query';
import { Link } from 'react-router-dom';
import { Users, Briefcase, Zap, Building2, GitGraph, TrendingUp, ChevronRight } from 'lucide-react';
import { fetchCandidates, fetchJobs, fetchSkillDemand, fetchCompanies, fetchHealth } from '../services/api';
import LoadingSpinner from '../components/LoadingSpinner';
import ErrorMessage from '../components/ErrorMessage';
import SkillBadge from '../components/SkillBadge';

export default function Dashboard() {
  const { data: health } = useQuery({ queryKey: ['health'], queryFn: fetchHealth });
  const { data: candidates, isLoading: loadingC } = useQuery({ queryKey: ['candidates'], queryFn: fetchCandidates });
  const { data: jobs, isLoading: loadingJ } = useQuery({ queryKey: ['jobs'], queryFn: fetchJobs });
  const { data: companies, isLoading: loadingCo } = useQuery({ queryKey: ['companies'], queryFn: fetchCompanies });
  const { data: demand, isLoading: loadingD } = useQuery({ queryKey: ['skill-demand'], queryFn: fetchSkillDemand });

  const dbDown = health?.database === 'unavailable';
  const loading = loadingC || loadingJ || loadingCo || loadingD;

  return (
    <div className="space-y-8">
      {/* Hero */}
      <div className="relative rounded-2xl overflow-hidden bg-gradient-to-br from-indigo-950 via-gray-900 to-gray-950 border border-indigo-800/30 p-8 md:p-12">
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top_right,_var(--tw-gradient-stops))] from-indigo-900/20 via-transparent to-transparent" />
        <div className="relative">
          <div className="flex items-center gap-2 text-indigo-400 mb-4">
            <GitGraph className="w-6 h-6" />
            <span className="text-sm font-medium uppercase tracking-widest">Graph-Powered Career Intelligence</span>
          </div>
          <h1 className="text-3xl md:text-5xl font-bold text-white mb-4 leading-tight">
            Explore how skills<br />
            <span className="text-indigo-400">connect people to careers</span>
          </h1>
          <p className="text-gray-400 text-lg max-w-2xl mb-6">
            SkillGraph uses a graph database to reveal hidden connections between skills, jobs, and companies.
            Discover multi-hop career paths and skill gaps that flat job boards can't show you.
          </p>
          <div className="flex flex-wrap gap-3">
            <Link to="/candidates" className="inline-flex items-center gap-2 px-5 py-2.5 bg-indigo-600 hover:bg-indigo-500 text-white rounded-xl font-medium transition-colors">
              <Users className="w-4 h-4" /> Explore Candidates
            </Link>
            <Link to="/skills" className="inline-flex items-center gap-2 px-5 py-2.5 bg-gray-800 hover:bg-gray-700 text-white rounded-xl font-medium transition-colors">
              <Zap className="w-4 h-4" /> Skill Demand
            </Link>
          </div>
        </div>
      </div>

      {/* DB Status */}
      {dbDown && (
        <ErrorMessage
          title="Graph database unavailable"
          message="Could not connect to CognoDB. Some data may not load correctly. Please check your configuration."
        />
      )}

      {/* Stats */}
      {loading ? (
        <LoadingSpinner message="Loading graph data..." />
      ) : (
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {[
            { label: 'Candidates', value: candidates?.length ?? 0, icon: Users, to: '/candidates', color: 'text-indigo-400' },
            { label: 'Open Jobs', value: jobs?.length ?? 0, icon: Briefcase, to: '/jobs', color: 'text-emerald-400' },
            { label: 'Companies', value: companies?.length ?? 0, icon: Building2, to: '/companies', color: 'text-amber-400' },
            { label: 'Skills Tracked', value: demand?.length ?? 0, icon: Zap, to: '/skills', color: 'text-violet-400' },
          ].map(({ label, value, icon: Icon, to, color }) => (
            <Link key={label} to={to} className="group bg-gray-900 border border-gray-800 rounded-xl p-5 hover:border-indigo-700 transition-colors">
              <div className="flex items-center justify-between mb-3">
                <Icon className={`w-5 h-5 ${color}`} />
                <ChevronRight className="w-4 h-4 text-gray-600 group-hover:text-indigo-400 transition-colors" />
              </div>
              <div className="text-3xl font-bold text-white">{value}</div>
              <div className="text-sm text-gray-500 mt-1">{label}</div>
            </Link>
          ))}
        </div>
      )}

      {/* Top Skills & Recent Jobs */}
      <div className="grid md:grid-cols-2 gap-6">
        {/* Top Demanded Skills */}
        <div className="bg-gray-900 border border-gray-800 rounded-xl p-6">
          <div className="flex items-center gap-2 mb-5">
            <TrendingUp className="w-5 h-5 text-indigo-400" />
            <h2 className="font-semibold text-white">Most Demanded Skills</h2>
          </div>
          {loadingD ? <LoadingSpinner size="sm" /> : (
            <div className="space-y-3">
              {demand?.slice(0, 8).map((s) => (
                <div key={s.id} className="flex items-center justify-between gap-3">
                  <SkillBadge name={s.name} category={s.category} />
                  <div className="flex items-center gap-3 text-sm">
                    <span className="text-gray-500">{s.job_count} jobs</span>
                    <div className="w-24 h-1.5 bg-gray-800 rounded-full overflow-hidden">
                      <div
                        className="h-full bg-indigo-500 rounded-full"
                        style={{ width: `${Math.min(100, (s.job_count / (demand?.[0]?.job_count || 1)) * 100)}%` }}
                      />
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
          <Link to="/skills" className="inline-flex items-center gap-1 mt-4 text-sm text-indigo-400 hover:text-indigo-300">
            View all skills <ChevronRight className="w-3 h-3" />
          </Link>
        </div>

        {/* Recent candidates */}
        <div className="bg-gray-900 border border-gray-800 rounded-xl p-6">
          <div className="flex items-center gap-2 mb-5">
            <Users className="w-5 h-5 text-indigo-400" />
            <h2 className="font-semibold text-white">Candidates</h2>
          </div>
          {loadingC ? <LoadingSpinner size="sm" /> : (
            <div className="space-y-3">
              {candidates?.slice(0, 6).map((c) => (
                <Link key={c.id} to={`/candidates/${c.id}`}
                  className="flex items-center gap-3 p-2 rounded-lg hover:bg-gray-800 transition-colors group"
                >
                  <div className="w-9 h-9 rounded-full bg-indigo-900/50 border border-indigo-700/50 flex items-center justify-center text-indigo-300 font-bold text-sm flex-shrink-0">
                    {c.name[0]}
                  </div>
                  <div className="min-w-0">
                    <p className="text-sm font-medium text-white group-hover:text-indigo-300 truncate">{c.name}</p>
                    <p className="text-xs text-gray-500">{c.experience_years}y · {c.location}</p>
                  </div>
                  <ChevronRight className="w-4 h-4 text-gray-600 ml-auto flex-shrink-0 group-hover:text-indigo-400" />
                </Link>
              ))}
            </div>
          )}
          <Link to="/candidates" className="inline-flex items-center gap-1 mt-4 text-sm text-indigo-400 hover:text-indigo-300">
            View all candidates <ChevronRight className="w-3 h-3" />
          </Link>
        </div>
      </div>
    </div>
  );
}
