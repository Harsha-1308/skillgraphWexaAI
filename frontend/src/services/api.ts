import axios from 'axios';
import type {
  Candidate, Job, JobDetail, Company, CompanyDetail,
  Skill, SkillWithRelated, SkillDemand, JobMatch,
  SkillGapAnalysis, RoleDiscovery, SkillBridgePath, HealthStatus
} from '../types';

const BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: `${BASE_URL}/api`,
  timeout: 15000,
});

// Candidates
export const fetchCandidates = () =>
  api.get<Candidate[]>('/candidates').then(r => r.data);

export const fetchCandidate = (id: string) =>
  api.get<Candidate>(`/candidates/${id}`).then(r => r.data);

export const fetchCandidateSkills = (id: string) =>
  api.get<Skill[]>(`/candidates/${id}/skills`).then(r => r.data);

export const fetchCandidateJobs = (id: string) =>
  api.get<{ direct_matches: JobMatch[]; extended_matches: JobMatch[] }>(`/candidates/${id}/jobs`).then(r => r.data);

export const fetchSkillGap = (candidateId: string, jobId: string) =>
  api.get<SkillGapAnalysis>(`/candidates/${candidateId}/skill-gaps/${jobId}`).then(r => r.data);

export const fetchCandidateRoles = (id: string) =>
  api.get<RoleDiscovery[]>(`/candidates/${id}/roles`).then(r => r.data);

// Jobs
export const fetchJobs = () =>
  api.get<Job[]>('/jobs').then(r => r.data);

export const fetchJob = (id: string) =>
  api.get<JobDetail>(`/jobs/${id}`).then(r => r.data);

// Skills
export const fetchSkills = () =>
  api.get<Skill[]>('/skills').then(r => r.data);

export const fetchSkillDemand = () =>
  api.get<SkillDemand[]>('/skills/demand').then(r => r.data);

export const fetchRelatedSkills = (id: string) =>
  api.get<SkillWithRelated>(`/skills/${id}/related`).then(r => r.data);

// Companies
export const fetchCompanies = () =>
  api.get<Company[]>('/companies').then(r => r.data);

export const fetchCompany = (id: string) =>
  api.get<CompanyDetail>(`/companies/${id}`).then(r => r.data);

// Graph
export const fetchSkillBridge = (candidateId: string, jobId: string) =>
  api.get<SkillBridgePath[]>(`/graph/skill-bridge/${candidateId}/${jobId}`).then(r => r.data);

// Health
export const fetchHealth = () =>
  api.get<HealthStatus>('/health').then(r => r.data);
