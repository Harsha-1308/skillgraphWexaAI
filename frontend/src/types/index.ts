export interface Candidate {
  id: string;
  name: string;
  email: string;
  experience_years: number;
  location: string;
  bio: string;
  skills?: Skill[];
}

export interface Skill {
  id: string;
  name: string;
  category: string;
  level: string;
  candidate_level?: string;
  years?: number;
}

export interface RelatedSkill extends Skill {
  strength: number;
  hops: number;
}

export interface SkillWithRelated extends Skill {
  related: RelatedSkill[];
}

export interface Company {
  id: string;
  name: string;
  industry: string;
  description: string;
  location: string;
  job_count?: number;
}

export interface CompanyDetail extends Company {
  jobs: JobInCompany[];
  total_jobs: number;
  top_skills: string[];
}

export interface JobInCompany {
  id: string;
  title: string;
  employment_type: string;
  experience_required: number;
  required_skills: string[];
}

export interface Job {
  id: string;
  title: string;
  description: string;
  experience_required: number;
  location: string;
  employment_type: string;
  salary_min?: number;
  salary_max?: number;
  company_id: string;
  company_name: string;
}

export interface JobDetail extends Job {
  required_skills: RequiredSkill[];
  role_name?: string;
}

export interface RequiredSkill {
  id: string;
  name: string;
  category: string;
  minimum_level: string;
  importance: string;
}

export interface JobMatch {
  job: Job;
  matched_skills: string[];
  total_required: number;
  match_count: number;
  match_percentage: number;
  via_related: boolean;
}

export interface SkillGapItem {
  skill_id: string;
  skill_name: string;
  category: string;
  minimum_level: string;
  importance: string;
  candidate_level?: string;
  has_skill: boolean;
}

export interface SkillGapAnalysis {
  job_id: string;
  job_title: string;
  company_name: string;
  match_percentage: number;
  required_skills: SkillGapItem[];
  missing_skills: SkillGapItem[];
  matched_skills: SkillGapItem[];
}

export interface SkillDemand {
  id: string;
  name: string;
  category: string;
  level: string;
  job_count: number;
  company_count: number;
}

export interface RoleDiscovery {
  role_id: string;
  role_name: string;
  job_count: number;
  connecting_skills: string[];
}

export interface SkillBridgePath {
  from_skill: string;
  to_skill: string;
  hops: number;
  path_names: string[];
}

export interface HealthStatus {
  status: 'healthy' | 'degraded';
  database: 'connected' | 'unavailable';
  application: string;
  version: string;
}
