"use client";

import { useFrontendTool, useRenderToolCall, useCopilotChat, useCopilotReadable, useCoAgent } from "@copilotkit/react-core";
import { TextMessage, MessageRole } from "@copilotkit/runtime-client-gql";
import { CopilotKitCSSProperties, CopilotSidebar } from "@copilotkit/react-ui";
import { useState, useEffect } from "react";
import { AgentState } from "@/lib/types";
import { 
  Mail, Phone, Globe, MapPin, CheckCircle, 
  Award, Briefcase, UserCircle, GraduationCap, 
  Code, Heart, MessageSquare, AlertTriangle, RefreshCw, ChevronDown, ChevronUp
} from "lucide-react";

const INITIAL_SUMMARY = "Full stack engineer with 15+ years of experience building AgenticAI solutions and HPC clusters for LLM/ML training. Expert in LLMOps pipelines, high-availability model serving, and RESTful API development. Proven track record in Kubernetes (CKA), Infrastructure-as-Code (Terraform/Ansible), and managing software development from inception to production.";

export default function ProfilePage() {
  const [themeColor, setThemeColor] = useState("#2c3e50"); // Darker default from reference
  const [highlightedSection, setHighlightedSection] = useState<string | null>(null);
  const [summary, setSummary] = useState(INITIAL_SUMMARY);
  const [llmStatus, setLlmStatus] = useState<'checking' | 'ok' | 'error'>('checking');
  const [llmError, setLlmError] = useState<string | null>(null);
  const [showUsage, setShowUsage] = useState(false);

  const { appendMessage } = useCopilotChat();

  // Build health check URL based on current host
  const getHealthUrl = () => {
    if (typeof window === 'undefined') return 'http://localhost:8001/health';
    const host = window.location.hostname;
    return `http://${host}:8001/health`;
  };

  // Health check on mount and periodically
  useEffect(() => {
    const checkHealth = async () => {
      try {
        const response = await fetch(getHealthUrl(), { 
          method: 'GET',
          signal: AbortSignal.timeout(5000)
        });
        const data = await response.json();
        if (data.llm === 'ok' || data.llm === 'native_gemini') {
          setLlmStatus('ok');
          setLlmError(null);
        } else {
          setLlmStatus('error');
          setLlmError(data.llm || 'LLM service unavailable');
        }
      } catch (err) {
        setLlmStatus('error');
        setLlmError('Cannot connect to agent service');
      }
    };

    checkHealth();
    // Check every 30 seconds
    const interval = setInterval(checkHealth, 30000);
    return () => clearInterval(interval);
  }, []);

  const retryConnection = async () => {
    setLlmStatus('checking');
    try {
      const response = await fetch(getHealthUrl(), { 
        method: 'GET',
        signal: AbortSignal.timeout(5000)
      });
      const data = await response.json();
      if (data.llm === 'ok' || data.llm === 'native_gemini') {
        setLlmStatus('ok');
        setLlmError(null);
      } else {
        setLlmStatus('error');
        setLlmError(data.llm || 'LLM service unavailable');
      }
    } catch (err) {
      setLlmStatus('error');
      setLlmError('Cannot connect to agent service');
    }
  };

  const { state: agentState } = useCoAgent<AgentState>({
    name: "BharathAssistant",
    initialState: { conversation_context: [] }
  });

  useCopilotReadable({
    description: "The professional summary displayed on the profile page. Use this to understand Bharath's background.",
    value: summary,
  });

  // Frontend tool: Update summary
  useFrontendTool({
    name: "updateProfessionalSummary",
    description: "Update the professional summary section with new text.",
    parameters: [
      {
        name: "newSummary",
        description: "The new summary text to display.",
        required: true,
      },
    ],
    handler: ({ newSummary }: { newSummary: string }) => {
      setSummary(newSummary);
    },
  } as any);

  // Frontend tool: Set theme color
  useFrontendTool({
    name: "setThemeColor",
    description: "Change the theme color of the profile page",
    parameters: [
      {
        name: "themeColor",
        description: "The theme color to set (hex color code).",
        required: true,
      },
    ],
    handler({ themeColor }: { themeColor: string }) {
      setThemeColor(themeColor);
    },
  } as any);

  // Frontend tool: Highlight section
  useFrontendTool({
    name: "highlightSection",
    description: "Highlight a specific section of the profile and scroll to it",
    parameters: [
      {
        name: "section",
        description: "Section to highlight: contact, summary, education, experience, skills, certifications",
        required: true,
      },
    ],
    handler({ section }: { section: string }) {
      setHighlightedSection(section);
      const element = document.getElementById(section);
      if (element) {
        element.scrollIntoView({ behavior: "smooth", block: "start" });
        // Add a temporary flash effect class
        element.classList.add("bg-yellow-50");
        setTimeout(() => {
          setHighlightedSection(null);
          element.classList.remove("bg-yellow-50");
        }, 3000);
      }
    },
  } as any);

  // Frontend tool: Filter skills (Modified to just scroll/highlight since we show all)
  useFrontendTool({
    name: "filterSkills",
    description: "Highlight a specific skill category",
    parameters: [
      {
        name: "category",
        description: "Category to highlight",
        required: true,
      },
    ],
    handler({ category }: { category: string }) {
      const element = document.getElementById("skills");
      element?.scrollIntoView({ behavior: "smooth", block: "center" });
    },
  } as any);

  // Frontend tool: Expand experience details (Modified to just scroll since we show all)
  useFrontendTool({
    name: "showExperienceDetails",
    description: "Scroll to a specific job position",
    parameters: [
      {
        name: "experienceId",
        description: "Experience ID to scroll to (exp-1 through exp-7)",
        required: true,
      },
    ],
    handler({ experienceId }: { experienceId: string }) {
      const element = document.getElementById(experienceId);
      element?.scrollIntoView({ behavior: "smooth", block: "center" });
    },
  } as any);

  // Generative UI: Render conversation notes
  useRenderToolCall({
    name: "add_conversation_note",
    description: "Add a note about the current conversation",
    parameters: [],
    render: ({ args, status }: any) => {
      if (status === "complete") {
        return (
          <div className="p-3 bg-green-50 border-l-4 border-green-500 rounded-lg mb-4">
            <div className="flex items-start gap-2">
              <CheckCircle size={18} className="text-green-600 mt-0.5 flex-shrink-0" />
              <div>
                <p className="text-base font-semibold text-green-800">Note Added</p>
                <p className="text-base text-gray-700 mt-1">{args.note}</p>
              </div>
            </div>
          </div>
        );
      }
      return (
        <div className="p-3 bg-gray-50 rounded-lg mb-4">
          <p className="text-base text-gray-500">Adding note...</p>
        </div>
      );
    },
  });

  const handleAsk = (question: string) => {
    appendMessage(
      new TextMessage({
        id: Math.random().toString(36).substring(7),
        role: MessageRole.User,
        content: question,
      })
    );
  };

  return (
    <main
      style={
        { "--copilot-kit-primary-color": themeColor } as CopilotKitCSSProperties
      }
    >
      <CopilotSidebar
        disableSystemMessage={true}
        clickOutsideToClose={true}
        defaultOpen={false}
        labels={{
          title: "Bharath's Assistant",
          initial: "Hi! I'm Bharath's personal assistant. I can guide you through his 15 years of experience.",
        }}
        suggestions={[
          {
            title: "Experience",
            message: "How many years of experience does Bharath have?",
          },
          {
            title: "Current Role",
            message: "What is Bharath's current position?",
          },
          {
            title: "AgenticAI",
            message: "Tell me about Bharath's AgenticAI work",
          },
          {
            title: "LLM/ML",
            message: "What experience does Bharath have with LLMs and ML platforms?",
          },
          {
            title: "Kubernetes",
            message: "Tell me about Bharath's Kubernetes experience",
          },
          {
            title: "Leadership",
            message: "Has Bharath led teams or managed people?",
          },
          {
            title: "Infrastructure",
            message: "What's Bharath's experience with Terraform and Ansible?",
          },
          {
            title: "Education",
            message: "What is Bharath's educational background?",
          },
          {
            title: "Tokyo",
            message: "Tell me about Bharath's experience working in Tokyo",
          },
          {
            title: "Bioinformatics",
            message: "How did Bharath transition from bioinformatics to software engineering?",
          },
        ]}
      >
        {/* Floating session stats badge - inside sidebar to prevent close on click */}
        {agentState?.total_token_count && (
          <div className="fixed bottom-24 right-6 z-50">
            <div className="relative">
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  setShowUsage(!showUsage);
                }}
                className="flex items-center gap-2 px-3 py-2 bg-blue-600 text-white rounded-full text-xs font-medium hover:bg-blue-700 transition-all shadow-lg hover:shadow-xl"
                aria-label="Toggle session usage stats"
              >
                <span>📊 Session Stats</span>
                <ChevronDown size={14} className={`transition-transform duration-200 ${showUsage ? 'rotate-180' : ''}`} />
              </button>
              {showUsage && (
                <>
                  <div
                    className="fixed inset-0 z-40"
                    onClick={() => setShowUsage(false)}
                  />
                  <div
                    className="absolute bottom-full right-0 mb-2 w-56 rounded-md bg-white shadow-xl ring-1 ring-black ring-opacity-10 z-50"
                    onClick={(e) => e.stopPropagation()}
                  >
                    <div className="p-3">
                      <div className="flex flex-col gap-2 text-xs font-mono">
                        <div className="flex justify-between items-center border-b border-slate-200 pb-2">
                          <span className="text-slate-600 font-semibold uppercase tracking-wide text-[10px]">Session Usage</span>
                          <span className="text-slate-400">📊</span>
                        </div>
                        <div className="flex justify-between items-center">
                          <span className="text-slate-600">Total Tokens</span>
                          <span className="text-blue-600 font-bold bg-blue-50 px-2 py-1 rounded">{agentState.total_token_count.toLocaleString()}</span>
                        </div>
                        <div className="flex justify-between items-center">
                          <span className="text-slate-600">Context Size</span>
                          <span className="text-orange-600 font-bold bg-orange-50 px-2 py-1 rounded">{agentState.last_context_tokens || 0}</span>
                        </div>
                        <div className="flex justify-between items-center">
                          <span className="text-slate-600">Last Response</span>
                          <span className="text-purple-600 font-bold bg-purple-50 px-2 py-1 rounded">{agentState.last_response_tokens || 0}</span>
                        </div>
                        <div className="flex justify-between items-center">
                          <span className="text-slate-600">Speed</span>
                          <span className="text-green-600 font-bold bg-green-50 px-2 py-1 rounded">{agentState.tokens_per_second || 0} t/s</span>
                        </div>
                      </div>
                    </div>
                  </div>
                </>
              )}
            </div>
          </div>
        )}

        {/* LLM Status Badge - Small, top-right corner (below token stats if shown) */}
        {/* LLM Status Badges (moved to header) */}

        {/* Session Usage (moved to header) */}
        <div className="min-h-screen bg-gray-100 flex justify-center items-start p-0 md:p-8 print:p-0 font-sans text-slate-800">
          <div className="w-full max-w-[1400px] bg-white shadow-xl grid grid-cols-1 lg:grid-cols-[280px_1fr] min-h-[90vh] print:shadow-none print:grid-cols-[280px_1fr]">
            
            {/* SIDEBAR */}
            <aside className="bg-slate-50 border-r border-gray-200 p-6 flex flex-col gap-6 print:bg-white">
              {/* Header */}
              <div className="text-center border-b border-gray-200 pb-6">
                <img 
                  src="/profile.jpg" 
                  alt="Bharath Krishna" 
                  className="w-32 h-32 rounded-full object-cover mx-auto mb-4 border-4 border-white shadow-lg"
                />
                <h1 className="text-3xl font-bold text-slate-800 mb-1">Bharath Krishna</h1>
                <h2 className="text-base font-medium text-blue-600 uppercase tracking-wide">Full Stack Engineer & AgenticAI</h2>
              </div>

              {/* Contact */}
              <div id="contact" className="flex flex-col gap-3 text-base text-gray-600">
                <a href="mailto:bharath.chakravarthi@gmail.com" className="flex items-center gap-3 hover:text-blue-600 transition-colors p-2 hover:bg-blue-50 rounded-lg -ml-2">
                  <div className="w-8 h-8 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center">
                    <Mail size={16} />
                  </div>
                  <span>bharath.chakravarthi@gmail.com</span>
                </a>
                <a href="tel:+18574379316" className="flex items-center gap-3 hover:text-blue-600 transition-colors p-2 hover:bg-blue-50 rounded-lg -ml-2">
                  <div className="w-8 h-8 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center">
                    <Phone size={16} />
                  </div>
                  <span>+1-857-437-9316</span>
                </a>
                <a href="https://profile.krishb.in" target="_blank" className="flex items-center gap-3 hover:text-blue-600 transition-colors p-2 hover:bg-blue-50 rounded-lg -ml-2">
                  <div className="w-8 h-8 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center">
                    <Globe size={16} />
                  </div>
                  <span>profile.krishb.in</span>
                </a>
                <div className="flex items-center gap-3 p-2 -ml-2">
                  <div className="w-8 h-8 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center">
                    <MapPin size={16} />
                  </div>
                  <span>California, USA</span>
                </div>
              </div>

              {/* Skills */}
              <div id="skills" className="space-y-6">
                <h3 className="text-base font-bold uppercase text-slate-800 border-b-2 border-blue-500 inline-block pb-1">Technical Skills</h3>
                
                <div className="space-y-4">
                  <SkillGroup title="Core Strengths" skills={["LLMOps", "DevOps", "AgenticAI", "HA Systems", "Agile/Scrum"]} onAsk={handleAsk} />
                  <SkillGroup title="Languages" skills={["Python (15y)", "Golang (7y)"]} onAsk={handleAsk} />
                  <SkillGroup title="Frontend" skills={["React", "NextJS", "ChakraUI"]} onAsk={handleAsk} />
                  <SkillGroup title="Infrastructure" skills={["Kubernetes (CKA)", "Ansible", "Terraform", "GCP", "Docker"]} onAsk={handleAsk} />
                  <SkillGroup title="Backend" skills={["FastAPI", "Gin Gonic", "Postgres", "MongoDB"]} onAsk={handleAsk} />
                </div>
              </div>

              {/* Spoken Languages */}
              <div>
                <h3 className="text-base font-bold uppercase text-slate-800 border-b-2 border-blue-500 inline-block pb-1 mb-2">Spoken Languages</h3>
                <p className="text-sm text-gray-600">English, Hindi, Kannada, Telugu</p>
              </div>

              {/* Interests */}
              <div>
                <h3 className="text-base font-bold uppercase text-slate-800 border-b-2 border-blue-500 inline-block pb-1 mb-2">Interests</h3>
                <p className="text-sm text-gray-600">Gardening, Movies</p>
              </div>

              {/* Certs */}
              <div id="certifications">
                <h3 className="text-base font-bold uppercase text-slate-800 border-b-2 border-blue-500 inline-block pb-1 mb-2">Certifications</h3>
                <div className="flex items-start gap-2 text-base text-gray-700">
                  <Award size={16} className="mt-0.5 text-blue-600" />
                  <span>Certified Kubernetes Administrator (CKA)</span>
                </div>
              </div>

            </aside>

            {/* MAIN CONTENT */}
            <main className="p-8 flex flex-col gap-6">
              
              {/* Summary */}
              <section id="summary">
                <h3 className="flex items-center gap-2 text-xl font-bold text-slate-800 border-b border-gray-200 pb-2 mb-3">
                  <UserCircle className="text-blue-600" size={24} /> Professional Summary
                </h3>
                <p className="text-base text-gray-700 leading-relaxed text-justify">
                  {summary}
                </p>
              </section>

              {/* Education */}
              <section id="education">
                <h3 className="flex items-center gap-2 text-xl font-bold text-slate-800 border-b border-gray-200 pb-2 mb-2">
                  <GraduationCap className="text-blue-600" size={24} /> Education
                </h3>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="border-l-2 border-blue-500 pl-3">
                    <h4 className="font-bold text-slate-800 text-base leading-tight">M.Sc in Bioinformatics</h4>
                    <p className="text-sm text-blue-600 font-medium">Kuvempu University, Karnataka</p>
                    <p className="text-xs text-gray-500 mt-1">Focus: Genomics, Drug Discovery, Protein Engineering</p>
                  </div>

                  <div className="border-l-2 border-blue-500 pl-3">
                    <h4 className="font-bold text-slate-800 text-base leading-tight">B.Sc in Biotechnology</h4>
                    <p className="text-sm text-blue-600 font-medium">Kuvempu University, Karnataka</p>
                    <p className="text-xs text-gray-500 mt-1">Majors: Biotechnology, Botany, Computer Science</p>
                  </div>
                </div>
              </section>

              {/* Experience */}
              <section id="experience">
                <h3 className="flex items-center gap-2 text-xl font-bold text-slate-800 border-b border-gray-200 pb-2 mb-4">
                  <Briefcase className="text-blue-600" size={24} /> Experience
                </h3>
                
                <div className="flex flex-col gap-5">
                  <JobItem 
                    id="exp-7"
                    title="Senior Software Engineer"
                    company="@ Rakuten USA"
                    date="May 2022 - Present"
                    details={[
                      "Building AgenticAI solutions and managing LLM deployments for peak usage.",
                      "Developing UI/API/CLI apps for submitting training jobs to HPC clusters.",
                      "Setting up MLOps pipelines and maintaining high-performance K8s clusters.",
                      "Automating infrastructure with Terraform/Ansible; Managing IAM via Keycloak.",
                      "Writing custom K8s operators and managing a team of UI/Infra engineers."
                    ]}
                    onAsk={handleAsk}
                  />

                  <JobItem 
                    id="exp-6"
                    title="Application Engineer"
                    company="@ Rakuten, Inc. Tokyo"
                    date="Jan 2018 - May 2022"
                    details={[
                      "Built IaC using Terraform/Ansible; wrote custom Terraform plugins & GoLang SDKs.",
                      "Developed REST API toolkits (FastAPI/Gin) and Auth services (Keycloak/Kong).",
                      "Conducted load testing (Locust) and wrote test cases (Pytest)."
                    ]}
                    onAsk={handleAsk}
                  />

                  <JobItem 
                    id="exp-5"
                    title="Application Engineer"
                    company="@ Rakuten India"
                    date="Sep 2014 - Dec 2018"
                    details={[
                      "Built APIs for IaaS (VMware), DNS (Nominum), and Load Balancers (BigIP).",
                      "Led a 3-member team as Scrum Master; automated jobs via Apache Airflow."
                    ]}
                    onAsk={handleAsk}
                  />

                  <JobItem 
                    id="exp-4"
                    title="Associate IT Consultant"
                    company="@ ITC Infotech / Bosch"
                    date="Jan 2014 - Sep 2014"
                    details={[
                      "Automated support for SCM tools (MKS/ClearQuest); wrote PERL sync scripts."
                    ]}
                    onAsk={handleAsk}
                  />

                  <JobItem 
                    id="exp-3"
                    title="Software Engineer"
                    company="@ eHover Systems"
                    date="Apr 2013 - Jan 2014"
                    details={[
                      "Developed cloud-based personal surveillance systems (AWS S3/EC2/ZoneMinder).",
                      "Built web interface for surveillance data access using PHP and CodeIgniter."
                    ]}
                    onAsk={handleAsk}
                  />

                  <JobItem 
                    id="exp-2"
                    title="Project Assistant"
                    company="@ Kuvempu University"
                    date="Apr 2011 - Apr 2013"
                    details={[
                      "Developed Perl modules for molecular dynamic simulation of Endotoxin neutralizing proteins.",
                      "Built web application to analyze SBML files using Python bindings of LibSBML.",
                      "Tech: BioPython, BioPerl, LibSBML, Gromacs."
                    ]}
                    onAsk={handleAsk}
                  />

                  <JobItem 
                    id="exp-1"
                    title="Software Developer Intern"
                    company="@ IBAB"
                    date="Sep 2010 - Feb 2011"
                    details={[
                      "Built 'Mammalian Gene Expression Database'.",
                      "Developed web app for bio-curator data using PERL, MySQL, and JavaScript."
                    ]}
                    onAsk={handleAsk}
                  />
                </div>
              </section>

            </main>
          </div>
        </div>
      </CopilotSidebar>
    </main>
  );
}

function SkillGroup({ title, skills, onAsk }: { title: string; skills: string[]; onAsk: (q: string) => void }) {
  return (
    <div>
      <h4 className="text-xs font-bold text-slate-500 uppercase tracking-wider mb-2">{title}</h4>
      <div className="flex flex-wrap gap-2">
        {skills.map((skill, idx) => (
          <button 
            key={idx} 
            onClick={() => onAsk(`Tell me about Bharath's experience with ${skill}`)}
            className="px-3 py-1 rounded-full bg-white text-slate-700 text-sm font-medium border border-slate-200 shadow-sm hover:border-blue-300 hover:text-blue-600 hover:bg-blue-50 transition-colors cursor-pointer"
          >
            {skill}
          </button>
        ))}
      </div>
    </div>
  );
}

function JobItem({ id, title, company, date, details, onAsk }: { id: string; title: string; company: string; date: string; details: string[]; onAsk: (q: string) => void }) {
  return (
    <div id={id} className="relative pl-8 before:absolute before:left-0 before:top-2 before:w-3 before:h-3 before:bg-blue-600 before:rounded-full before:ring-4 before:ring-blue-100 hover:bg-slate-50 p-4 rounded-lg -ml-4 transition-colors duration-300 group">
      <div className="absolute left-[5px] top-5 bottom-0 w-0.5 bg-gray-200 -z-10 last:hidden"></div>
      
      <div className="flex flex-col sm:flex-row justify-between items-baseline mb-2">
        <div className="flex items-center gap-3 flex-wrap">
          <div>
            <h4 className="font-bold text-slate-800 text-lg leading-tight">{title}</h4> 
            <p className="font-medium text-blue-600 text-base">{company}</p>
          </div>
          <button 
            onClick={(e) => {
              e.stopPropagation();
              onAsk(`What did Bharath do at ${company.replace('@ ', '')}?`);
            }}
            className="flex items-center gap-1.5 px-3 py-1 bg-blue-50 text-blue-600 rounded-full text-xs font-medium hover:bg-blue-100 transition-colors"
            aria-label={`Ask AI about experience at ${company}`}
          >
            <MessageSquare size={14} />
            <span>Ask AI</span>
          </button>
        </div>
        <span className="text-sm font-medium text-slate-500 bg-slate-100 px-2 py-1 rounded whitespace-nowrap mt-2 sm:mt-0">{date}</span>
      </div>
      <ul className="space-y-1.5 mt-3">
        {details.map((item, idx) => (
          <li key={idx} className="flex items-start gap-2 text-base text-gray-700 leading-relaxed">
            <span className="text-blue-400 mt-1.5 text-xs">●</span>
            <span>{item}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}
