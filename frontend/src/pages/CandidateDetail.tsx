import { useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { ArrowLeft, Briefcase, Zap, Star, GitBranch, ChevronDown, ChevronUp } from 'lucide-react';
import {
  fetchCandidate, fetchCandidateJobs, fetchSkillGap,
  fetchCandidateRoles, fetchSkillBridge
} from '../services/api';
import LoadingSpinner from '../components/LoadingSpinner';
import ErrorMessage from '../components/ErrorMessage';
import EmptyState from '../components/EmptyState';
import SkillBadge from '../components/SkillBadge';
import MatchPercentageBar from '../components/MatchPercentageBar';
import type { JobMatch } from '../types';

export default function CandidateDetail() {
  const { id } = useParams<{ id: string }>();
  const [selectedJob, setSelectedJob] = useState<JobMatch | null>(null);
  const [showExtended, setShowExtended] = useState(false);

  const { data: candidate, isLoading, error } = useQuery({
    queryKey: ['candidate', id],
    queryFn: () => fetchCandidate(id!),
    enabled: !!id,
  });

  const { data: jobsData, isLoading: loadingJobs } = useQuery({
    queryKey: ['candidate-jobs', id],
    queryFn: () => fetchCandidateJobs(id!),
    enabled: !!id,
  });

  const { data: roles } = useQuery({
    queryKey: ['candidate-roles', id],
    queryFn: () => fetchCandidateRoles(id!),
    enabled: !!id,
  });

  const { data: gapData, isLoading: loadingGap } = useQuery({
    queryKey: ['skill-gap', id, selectedJob?.job.id],
    queryFn: () => fetchSkillGap(id!, selectedJob!.job.id),
    enabled: !!id && !!selectedJob,
  });

  const { data: bridgeData } = useQuery({
    queryKey: ['skill-bridge', id, selectedJob?.job.id],
    queryFn: () => fetchSkillBridge(id!, selectedJob!.job.id),
    enabled: !!id && !!selectedJob,
  });

  if (isLoading) return <LoadingSpinner message="Loading candidate profile..." />;
  if (error) return <ErrorMessage />;
  if (!candidate) return <EmptyState title="Candidate not found" />;

  const directMatches = jobsData?.direct_matches ?? [];
  const extendedMatches = jobsData?.extended_matches ?? [];
  const skills = candidate.skills ?? [];

  const skillsByCategory = skills.reduce((acc, s) => {
    const cat = s.category || 'Other';
    if (!acc[cat]) acc[cat] = [];
    acc[cat].push(s);
    return acc;
  }, {} as Record<string, typeof skills>);

  return (
    <div className="space-y-6">
      {/* Back */}
      <Link to="/candidates" className="inline-flex items-center gap-1.5 text-sm text-gray-400 hover:text-white">
        <ArrowLeft className="w-4 h-4" /> Back to candidates
      </Link>

      {/* Profile header */}
      <div className="bg-gray-900 border border-gray-800 rounded-xl p-6">
        <div className="flex items-start gap-4">
          <div className="w-14 h-14 rounded-full bg-indigo-900/60 border border-indigo-700/50 flex items-center justify-center text-indigo-300 font-bold text-2xl flex-shrink-0">
            {candidate.name[0]}
          </div>
          <div>
            <h1 className="text-2xl font-bold text-white">{candidate.name}</h1>
            <p className="text-gray-400 text-sm">{candidate.email}</p>
            <p className="text-gray-500 text-sm mt-0.5">{candidate.experience_years} years experience · {candidate.location}</p>
            <p className="text-gray-400 mt-3 text-sm max-w-2xl">{candidate.bio}</p>
          </div>
        </div>
      </div>

      <div className="grid lg:grid-cols-3 gap-6">
        {/* Left: Skills + Roles */}
        <div className="space-y-5">
          {/* Skills by category */}
          <div className="bg-gray-900 border border-gray-800 rounded-xl p-5">
            <div className="flex items-center gap-2 mb-4">
              <Zap className="w-4 h-4 text-indigo-400" />
              <h2 className="font-semibold text-white">Skills ({skills.length})</h2>
            </div>
            {skills.length === 0 ? (
              <EmptyState title="No skills on profile" />
            ) : (
              <div className="space-y-4">
                {Object.entries(skillsByCategory).map(([cat, catSkills]) => (
                  <div key={cat}>
                    <p className="text-xs font-medium text-gray-500 uppercase tracking-wider mb-2">{cat}</p>
                    <div className="flex flex-wrap gap-1.5">
                      {catSkills.map((s) => (
                        <div key={s.id} title={s.candidate_level ? `Your level: ${s.candidate_level}` : undefined}>
                          <SkillBadge name={s.name} category={s.category} />
                        </div>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Career path roles */}
          {roles && roles.length > 0 && (
            <div className="bg-gray-900 border border-gray-800 rounded-xl p-5">
              <div className="flex items-center gap-2 mb-4">
                <Star className="w-4 h-4 text-amber-400" />
                <h2 className="font-semibold text-white">Career Directions</h2>
              </div>
              <div className="space-y-2">
                {roles.map((r) => (
                  <div key={r.role_id} className="bg-gray-800 rounded-lg p-3">
                    <div className="flex items-center justify-between mb-1">
                      <span className="text-sm font-medium text-white">{r.role_name}</span>
                      <span className="text-xs text-emerald-400">{r.job_count} jobs</span>
                    </div>
                    <div className="flex flex-wrap gap-1">
                      {r.connecting_skills.slice(0, 3).map((s) => (
                        <span key={s} className="text-xs text-gray-400 bg-gray-700 rounded-full px-2 py-0.5">{s}</span>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Right: Job matches */}
        <div className="lg:col-span-2 space-y-5">
          {/* Direct matches */}
          <div className="bg-gray-900 border border-gray-800 rounded-xl p-5">
            <div className="flex items-center gap-2 mb-4">
              <Briefcase className="w-4 h-4 text-indigo-400" />
              <h2 className="font-semibold text-white">Matching Jobs</h2>
              <span className="ml-auto text-xs text-gray-500">{directMatches.length} direct matches</span>
            </div>
            {loadingJobs ? <LoadingSpinner size="sm" message="Finding matching jobs..." /> :
              directMatches.length === 0 ? <EmptyState title="No matching jobs found" description="This candidate doesn't have skills matching any jobs." /> :
              <div className="space-y-3">
                {directMatches.map((match) => (
                  <button
                    key={match.job.id}
                    onClick={() => setSelectedJob(selectedJob?.job.id === match.job.id ? null : match)}
                    className={`w-full text-left p-4 rounded-xl border transition-all ${
                      selectedJob?.job.id === match.job.id
                        ? 'border-indigo-600 bg-indigo-950/30'
                        : 'border-gray-800 bg-gray-800/40 hover:border-gray-700'
                    }`}
                  >
                    <div className="flex items-start justify-between gap-2 mb-2">
                      <div>
                        <p className="font-medium text-white">{match.job.title}</p>
                        <p className="text-sm text-gray-400">{match.job.company_name} · {match.job.location}</p>
                      </div>
                      <Link
                        to={`/companies/${match.job.company_id}`}
                        onClick={(e) => e.stopPropagation()}
                        className="text-xs text-indigo-400 hover:text-indigo-300 whitespace-nowrap"
                      >
                        View company
                      </Link>
                    </div>
                    <MatchPercentageBar percentage={match.match_percentage} />
                    <div className="mt-2">
                      <p className="text-xs text-gray-500 mb-1">{match.match_count}/{match.total_required} required skills matched</p>
                      <div className="flex flex-wrap gap-1">
                        {match.matched_skills.slice(0, 5).map((s) => (
                          <SkillBadge key={s} name={s} variant="matched" />
                        ))}
                        {match.matched_skills.length > 5 && (
                          <span className="text-xs text-gray-500">+{match.matched_skills.length - 5} more</span>
                        )}
                      </div>
                    </div>
                  </button>
                ))}
              </div>
            }
          </div>

          {/* Extended matches via related skills */}
          {extendedMatches.length > 0 && (
            <div className="bg-gray-900 border border-gray-800 rounded-xl p-5">
              <button
                onClick={() => setShowExtended(!showExtended)}
                className="flex items-center gap-2 w-full"
              >
                <GitBranch className="w-4 h-4 text-violet-400" />
                <h2 className="font-semibold text-white">Extended Matches via Related Skills</h2>
                <span className="ml-auto text-xs text-violet-400">{extendedMatches.length} jobs (multi-hop)</span>
                {showExtended ? <ChevronUp className="w-4 h-4 text-gray-400" /> : <ChevronDown className="w-4 h-4 text-gray-400" />}
              </button>
              {showExtended && (
                <div className="mt-4 space-y-3">
                  <p className="text-xs text-gray-500 bg-violet-950/30 border border-violet-800/30 rounded-lg p-3">
                    These jobs are reachable via a 3-hop graph traversal: <strong className="text-violet-300">Candidate → HAS_SKILL → Skill → RELATED_TO → Skill → REQUIRES_SKILL ← Job</strong>.
                    You don't have the required skills directly, but your existing skills are related to what these jobs need.
                  </p>
                  {extendedMatches.map((match) => (
                    <button
                      key={match.job.id}
                      onClick={() => setSelectedJob(selectedJob?.job.id === match.job.id ? null : match)}
                      className={`w-full text-left p-4 rounded-xl border transition-all ${
                        selectedJob?.job.id === match.job.id
                          ? 'border-violet-600 bg-violet-950/20'
                          : 'border-gray-800 bg-gray-800/40 hover:border-gray-700'
                      }`}
                    >
                      <div className="flex items-start justify-between gap-2 mb-2">
                        <div>
                          <p className="font-medium text-white">{match.job.title}</p>
                          <p className="text-sm text-gray-400">{match.job.company_name}</p>
                        </div>
                        <span className="text-xs text-violet-400 border border-violet-700/50 rounded-full px-2 py-0.5">via related skills</span>
                      </div>
                      <div className="flex flex-wrap gap-1">
                        {match.matched_skills.slice(0, 4).map((s) => (
                          <SkillBadge key={s} name={s} variant="related" />
                        ))}
                      </div>
                    </button>
                  ))}
                </div>
              )}
            </div>
          )}

          {/* Skill gap analysis */}
          {selectedJob && (
            <div className="bg-gray-900 border border-indigo-800/40 rounded-xl p-5">
              <h2 className="font-semibold text-white mb-1">Skill Gap Analysis</h2>
              <p className="text-sm text-gray-400 mb-4">
                {selectedJob.job.title} at {selectedJob.job.company_name}
              </p>
              {loadingGap ? <LoadingSpinner size="sm" message="Analysing skill gap..." /> :
                gapData ? (
                  <div className="space-y-4">
                    <div className="flex items-center gap-3">
                      <MatchPercentageBar percentage={gapData.match_percentage} />
                    </div>
                    <div className="grid sm:grid-cols-2 gap-4">
                      {/* Matched */}
                      {gapData.matched_skills.length > 0 && (
                        <div>
                          <p className="text-xs font-medium text-emerald-400 uppercase tracking-wider mb-2">✓ Skills You Have</p>
                          <div className="space-y-1.5">
                            {gapData.matched_skills.map((s) => (
                              <div key={s.skill_id} className="flex items-center justify-between text-sm">
                                <SkillBadge name={s.skill_name} variant="matched" />
                                <span className="text-xs text-gray-500">{s.candidate_level}</span>
                              </div>
                            ))}
                          </div>
                        </div>
                      )}
                      {/* Missing */}
                      {gapData.missing_skills.length > 0 && (
                        <div>
                          <p className="text-xs font-medium text-red-400 uppercase tracking-wider mb-2">✗ Skills to Learn</p>
                          <div className="space-y-1.5">
                            {gapData.missing_skills.map((s) => (
                              <div key={s.skill_id} className="flex items-center justify-between text-sm">
                                <SkillBadge name={s.skill_name} variant="missing" />
                                <span className="text-xs text-amber-500">{s.importance}</span>
                              </div>
                            ))}
                          </div>
                        </div>
                      )}
                    </div>

                    {/* Skill bridge */}
                    {!selectedJob.via_related && bridgeData && bridgeData.length > 0 && (
                      <div className="mt-4 p-4 bg-indigo-950/30 border border-indigo-800/30 rounded-lg">
                        <p className="text-xs font-medium text-indigo-400 uppercase tracking-wider mb-2">🔗 Skill Bridge Paths</p>
                        <p className="text-xs text-gray-500 mb-3">Your existing skills that are related to required skills:</p>
                        <div className="space-y-2">
                          {bridgeData.slice(0, 5).map((b, i) => (
                            <div key={i} className="flex items-center gap-1 text-xs">
                              {b.path_names.map((name, j) => (
                                <span key={j} className="flex items-center gap-1">
                                  <span className={j === 0 ? 'text-emerald-400' : j === b.path_names.length - 1 ? 'text-amber-400' : 'text-violet-400'}>
                                    {name}
                                  </span>
                                  {j < b.path_names.length - 1 && <span className="text-gray-600">→</span>}
                                </span>
                              ))}
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                ) : null
              }
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
