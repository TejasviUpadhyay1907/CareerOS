'use client';

import { Code, Users, Wrench } from 'lucide-react';

interface Skill {
  name: string;
  category: string;
  proficiency?: string;
  is_primary?: boolean;
}

interface SkillsGridProps {
  skills: Skill[];
}

export function SkillsGrid({ skills }: SkillsGridProps) {
  const getCategoryIcon = (category: string) => {
    switch (category.toLowerCase()) {
      case 'technical':
        return <Code className="w-4 h-4" />;
      case 'soft':
        return <Users className="w-4 h-4" />;
      case 'tools':
        return <Wrench className="w-4 h-4" />;
      default:
        return <Code className="w-4 h-4" />;
    }
  };

  const getCategoryColor = (category: string) => {
    switch (category.toLowerCase()) {
      case 'technical':
        return 'bg-blue-100 text-blue-700 dark:bg-blue-900 dark:text-blue-300';
      case 'soft':
        return 'bg-purple-100 text-purple-700 dark:bg-purple-900 dark:text-purple-300';
      case 'tools':
        return 'bg-green-100 text-green-700 dark:bg-green-900 dark:text-green-300';
      default:
        return 'bg-gray-100 text-gray-700 dark:bg-gray-900 dark:text-gray-300';
    }
  };

  const groupedSkills = skills.reduce((acc, skill) => {
    const category = skill.category || 'other';
    if (!acc[category]) {
      acc[category] = [];
    }
    acc[category].push(skill);
    return acc;
  }, {} as Record<string, Skill[]>);

  if (skills.length === 0) {
    return (
      <div className="border rounded-xl p-6 text-center text-gray-500 dark:text-gray-400">
        No skills detected
      </div>
    );
  }

  return (
    <div className="border rounded-xl p-6 space-y-6">
      <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100">
        Skills
      </h3>

      {Object.entries(groupedSkills).map(([category, categorySkills]) => (
        <div key={category} className="space-y-3">
          <div className="flex items-center space-x-2">
            <div className={`p-2 rounded-lg ${getCategoryColor(category)}`}>
              {getCategoryIcon(category)}
            </div>
            <h4 className="font-medium text-gray-700 dark:text-gray-300 capitalize">
              {category}
            </h4>
            <span className="text-sm text-gray-500 dark:text-gray-400">
              ({categorySkills.length})
            </span>
          </div>

          <div className="flex flex-wrap gap-2">
            {categorySkills.map((skill) => (
              <div
                key={skill.name}
                className={`
                  px-3 py-1.5 rounded-full text-sm font-medium
                  ${skill.is_primary ? 'ring-2 ring-blue-500 ring-offset-2' : ''}
                  ${getCategoryColor(category)}
                `}
              >
                {skill.name}
                {skill.proficiency && (
                  <span className="ml-1 opacity-75">({skill.proficiency})</span>
                )}
              </div>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}
