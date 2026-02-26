export interface LeadScore {
  score: number; // 0 to 1
  reason: string;
  confidence: 'high' | 'medium' | 'low';
}

/**
 * Score a lead by fit, budget, seriousness
 * Returns: LeadScore (0-1 scale)
 */
export function scoreLead(content: string): LeadScore {
  const text = content.toLowerCase();
  let score = 0;
  const reasons: string[] = [];

  // Budget indicators (high confidence)
  if (text.includes('budget') || text.includes('$') || text.includes('usdt') || text.includes('sol')) {
    score += 0.3;
    reasons.push('budget_mentioned');
  }

  if (text.includes('ready to pay') || text.includes('paid project')) {
    score += 0.2;
    reasons.push('payment_ready');
  }

  // Urgency indicators (medium confidence)
  if (text.includes('asap') || text.includes('need this now') || text.includes('urgently') || text.includes('deadline')) {
    score += 0.2;
    reasons.push('urgency');
  }

  // Niche fit indicators (high confidence)
  const nicheKeywords = [
    'ai agent', 'automation', 'discord', 'workflow', 'lead-gen',
    'typescript', 'openclaw', 'chatbot', 'bot', 'assistant'
  ];
  
  const hasNiche = nicheKeywords.some(keyword => text.includes(keyword));
  if (hasNiche) {
    score += 0.15;
    reasons.push('niche_fit');
  }

  // Serious indicators (medium confidence)
  if (text.includes('looking for') || text.includes('need') || text.includes('help')) {
    score += 0.1;
    reasons.push('explicit_request_for_help');
  }

  if (text.includes('agency') || text.includes('dev') || text.includes('developer')) {
    score += 0.1;
    reasons.push('looking_for_agency');
  }

  // Confidence based on score
  let confidence: 'high' | 'medium' | 'low';
  if (score >= 0.7) confidence = 'high';
  else if (score >= 0.4) confidence = 'medium';
  else confidence = 'low';

  return {
    score: Math.round(score * 100) / 100, // round to 2 decimals
    reason: reasons.join(', '),
    confidence
  };
}

/**
 * Filter leads by threshold
 * Returns: leads that pass the score threshold
 */
export function filterLeads(leads: LeadScore[], threshold: number = 0.6): LeadScore[] {
  return leads.filter(lead => lead.score >= threshold);
}