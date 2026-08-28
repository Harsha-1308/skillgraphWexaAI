import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { Zap, TrendingUp } from 'lucide-react';
import { fetchSkillDemand, fetchRelatedSkills } from '../services/api';
import LoadingSpinner from '../components/LoadingSpinner';
import ErrorMessage from '../components/ErrorMessage';
import SkillBadge from '../components/SkillBadge';

export default function SkillsPage() {
  const [selectedSkill, setSelectedSkill] = useState<string | null>(null);

  const { data: demand, isLoading, error } = useQuery({
    queryKey: ['skill-demand'],
    queryFn: fetchSkillDemand,
  });

  const { data: related, isLoading: loadingRelated } = useQuery({
    queryKey: ['related-skills', selectedSkill],
    queryFn: () => fetchRelatedSkills(selectedSkill!),
    enabled: !!selectedSkill,
  });

  if (isLoading) return <LoadingSpinner message="Loading skill demand..." />;
  if (error) return <ErrorMessage />;

  const maxCount = demand?.[0]?.job_count ?? 1;

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white">Skills</h1>
        <p className="text-gray-400 mt-1">Demand across the job market. Click a skill to explore related skills.</p>
      </div>

      <div className="grid lg:grid-cols-3 gap-6">
        {/* Skill demand chart */}
        <div className="lg:col-span-2 bg-gray-900 border border-gray-800 rounded-xl p-5">
          <div className="flex items-center gap-2 mb-5">
            <TrendingUp className="w-5 h-5 text-indigo-400" />
            <h2 className="font-semibold text-white">Skill Demand</h2>
          </div>
          <div className="space-y-3">
            {demand?.map((s) => (
              <button
                key={s.id}
                onClick={() => setSelectedSkill(selectedSkill === s.id ? null : s.id)}
                className={`w-full text-left p-3 rounded-lg border transition-all ${
                  selectedSkill === s.id
                    ? 'border-indigo-600 bg-indigo-950/30'
                    : 'border-transparent hover:bg-gray-800'
                }`}
              >
                <div className="flex items-center justify-between gap-3 mb-1.5">
                  <div className="flex items-center gap-2">
                    <SkillBadge name={s.name} category={s.category} />
                  </div>
                  <div className="flex items-center gap-2 text-xs text-gray-500">
                    <span>{s.job_count} jobs</span>
                    <span>·</span>
                    <span>{s.company_count} companies</span>
                  </div>
                </div>
                <div className="h-1.5 bg-gray-800 rounded-full overflow-hidden">
                  <div
                    className="h-full bg-indigo-500 rounded-full transition-all"
                    style={{ width: `${(s.job_count / maxCount) * 100}%` }}
                  />
                </div>
              </button>
            ))}
          </div>
        </div>

        {/* Related skills panel */}
        <div className="bg-gray-900 border border-gray-800 rounded-xl p-5">
          <div className="flex items-center gap-2 mb-4">
            <Zap className="w-4 h-4 text-violet-400" />
            <h2 className="font-semibold text-white">Related Skills</h2>
          </div>
          {!selectedSkill ? (
            <p className="text-sm text-gray-500">Select a skill to see its related skills via graph traversal (up to 3 hops).</p>
          ) : loadingRelated ? (
            <LoadingSpinner size="sm" message="Traversing skill graph..." />
          ) : related?.related.length === 0 ? (
            <p className="text-sm text-gray-500">No related skills found for this skill.</p>
          ) : (
            <div className="space-y-3">
              <p className="text-sm font-medium text-white mb-2">{related?.name}</p>
              {related?.related.map((r) => (
                <div key={r.id} className="flex items-center justify-between p-2 bg-gray-800 rounded-lg">
                  <div className="flex items-center gap-2">
                    <SkillBadge name={r.name} category={r.category} />
                    <span className="text-xs text-gray-500">{r.hops} hop{r.hops > 1 ? 's' : ''}</span>
                  </div>
                  <div className="flex items-center gap-1 text-xs">
                    <div className="w-12 h-1 bg-gray-700 rounded-full overflow-hidden">
                      <div className="h-full bg-violet-500 rounded-full" style={{ width: `${r.strength * 100}%` }} />
                    </div>
                    <span className="text-gray-600">{(r.strength * 100).toFixed(0)}%</span>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
