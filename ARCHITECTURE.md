# System Architecture

## Overview

The Agentic SLA Orchestrator is built on a **governance-first, event-driven architecture** that combines deterministic rule systems with LLM intelligence for enterprise-grade reliability and contextual understanding.

---

## Design Principles

### 1. Governance First
- Action boundaries defined BEFORE AI integration
- Finite action catalog (no arbitrary invention)
- Risk-stratified approval workflows
- Audit trails and explainability

### 2. Hybrid Intelligence
- **60% Rules:** Deterministic, reliable, fast
- **40% LLM:** Contextual, adaptive, intelligent
- Strategic balance between reliability and insight

### 3. Human-in-the-Loop
- Medium/high risk actions require approval
- Learning from human decisions
- Trust earned through iteration (55% → 72%)

### 4. Event-Driven
- Proactive intervention (not reactive firefighting)
- 70% SLA threshold for early detection
- Temporal reasoning over ticket lifecycle

---

## System Layers

```
┌─────────────────────────────────────────────────────────────┐
│  APPLICATION LAYER                                          │
│  • Jupyter Notebooks (analysis, orchestration)              │
│  • Streamlit Dashboard (monitoring, approval interface)     │
│  • CLI Tools (batch processing, admin)                      │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│  ORCHESTRATION LAYER                                        │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │  Event   │→ │   Risk   │→ │   AI     │→ │  Action  │   │
│  │Processor │  │ Detector │  │ Decision │  │ Selector │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│  AI/ML LAYER                                                │
│  ┌──────────────┐         ┌──────────────┐                 │
│  │ LLM Service  │         │ Rules Engine │                 │
│  │ (GPT-4)      │    +    │ (Deterministic)                │
│  │              │         │              │                 │
│  └──────────────┘         └──────────────┘                 │
│         ↓                        ↓                          │
│  ┌─────────────────────────────────────┐                   │
│  │   Hybrid Confidence Engine          │                   │
│  │   (60% rules + 40% LLM)             │                   │
│  └─────────────────────────────────────┘                   │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│  DATA LAYER                                                 │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │ Tickets  │  │ Outcomes │  │  Events  │  │ Proposals│   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
└─────────────────────────────────────────────────────────────┘
```

---

## Component Details

### Data Foundation

**Purpose:** Provide clean, validated, policy-enriched data for orchestration

**Components:**
1. **Tickets Table** (stable context)
   - ticket_id, created_at, category, priority
   - subject, description, channel, assigned_agent

2. **Outcomes Table** (policy-based targets)
   - ticket_id, resolution_time_hours
   - sla_target_hours (from policy)
   - sla_breached (boolean)
   - csat (customer satisfaction)

3. **Events Table** (temporal reasoning)
   - event_id, ticket_id, event_type, event_time
   - Types: created, assigned, in_progress, resolved
   - Risk metrics: elapsed_hours, remaining_hours, urgency_score

**Data Contract:**
```python
# Assertions enforced
assert tickets['ticket_id'].isna().sum() == 0
assert outcomes['sla_target_hours'].isna().sum() == 0
assert events['event_time'].dtype == 'datetime64[ns]'
```

---

### Event Processor

**Purpose:** Convert snapshots to event streams for temporal reasoning

**Algorithm:**
```python
def construct_event_timeline(ticket_snapshot):
    """
    Generate 4-event lifecycle from resolution snapshot.
    
    Timeline:
    - created (t=0)
    - assigned (t=40% of total)
    - in_progress (t=60% of total)
    - resolved (t=100%)
    """
    total_hours = ticket_snapshot['resolution_time_hours']
    created_at = ticket_snapshot['submission_date']
    
    events = [
        {'type': 'created', 'time': created_at},
        {'type': 'assigned', 'time': created_at + 0.40 * total_hours},
        {'type': 'in_progress', 'time': created_at + 0.60 * total_hours},
        {'type': 'resolved', 'time': created_at + total_hours}
    ]
    
    return events
```

**Output:** 80,000 events from 20,000 tickets

---

### Risk Detector

**Purpose:** Identify intervention candidates based on SLA consumption

**Algorithm:**
```python
def calculate_risk_level(event, sla_target_hours):
    """
    Classify risk level based on SLA consumption percentage.
    
    Thresholds:
    - < 50% consumed: LOW (monitor only)
    - 50-70% consumed: MEDIUM (watch list)
    - > 70% consumed: HIGH (intervention required)
    - > 100% consumed: BREACHED (post-mortem)
    """
    elapsed = (event.time - ticket.created_at).total_seconds() / 3600
    remaining = sla_target_hours - elapsed
    pct_consumed = elapsed / sla_target_hours
    
    if remaining < 0:
        return 'breached'
    elif pct_consumed >= 0.70:
        return 'high'  # INTERVENTION CANDIDATE
    elif pct_consumed >= 0.50:
        return 'medium'
    else:
        return 'low'
```

**Threshold Rationale:**
- **70%** chosen as intervention point based on analysis:
  - Too early (30%): Alert fatigue, unnecessary interruptions
  - Too late (90%): Insufficient time to act
  - Sweet spot (70%): Maximum effectiveness with minimal noise

**Output:** 1,474 intervention candidates (7.4% of tickets)

---

### Hybrid Confidence Engine

**Purpose:** Combine rule-based reliability with LLM contextual intelligence

**Architecture:**

```python
def calculate_hybrid_confidence(ticket, event, action_type):
    """
    Hybrid confidence calculation combining rules and LLM.
    
    Formula:
    confidence = (0.6 × rule_urgency + 0.4 × llm_urgency 
                  - action_penalty) × llm_confidence_multiplier
    
    Returns: Float in range [0.3, 0.95]
    """
    
    # 1. Rule-based urgency (deterministic, fast)
    remaining_hours = sla_target - elapsed_hours
    rule_urgency = 1 - (remaining_hours / sla_target)
    rule_urgency = clip(rule_urgency, 0, 1)
    
    # 2. LLM-based urgency (contextual, slower)
    llm_response = classify_ticket_with_llm(
        description=ticket.description,
        subject=ticket.subject
    )
    llm_urgency = llm_response['urgency_score'] / 10.0  # normalize 0-10 → 0-1
    llm_confidence = llm_response['confidence']  # how sure is LLM?
    
    # 3. Weighted combination (60% rules, 40% LLM)
    base_confidence = (0.6 * rule_urgency) + (0.4 * llm_urgency)
    
    # 4. Apply action-specific penalty
    ACTION_PENALTY = {
        'escalate_to_supervisor_queue': 0.05,  # low disruption
        'reassign_ticket': 0.15,               # medium disruption
        'contact_customer': 0.20,              # high disruption
        'flag_stale_ticket': 0.00,             # no disruption
        # ... other actions
    }
    penalty = ACTION_PENALTY.get(action_type, 0.10)
    
    # 5. Apply LLM confidence as trust multiplier
    trust_multiplier = 0.8 + (0.2 * llm_confidence)
    
    # 6. Calculate final confidence
    final_confidence = (base_confidence - penalty) * trust_multiplier
    final_confidence = clip(final_confidence, 0.3, 0.95)
    
    return final_confidence
```

**Why 60/40 Split?**

| Aspect | Rules (60%) | LLM (40%) | Combined |
|--------|-------------|-----------|----------|
| **Reliability** | 100% deterministic | ~90% consistent | 96% |
| **Context** | None | Rich understanding | Moderate |
| **Speed** | <1ms | ~500ms | ~500ms |
| **Cost** | $0 | $0.0024/call | $0.0024/call |

Strategic tradeoff: Maximize reliability while capturing essential context.

---

### Action Governance

**Purpose:** Ensure all agent actions operate within safe boundaries

**Action Catalog** (finite, enumerated):

```python
ACTION_CATALOG = {
    'escalate_to_supervisor_queue': {
        'risk_tier': 'medium',
        'requires_approval': True,
        'penalty': 0.05,
        'description': 'Route ticket to supervisor attention queue'
    },
    'reassign_ticket': {
        'risk_tier': 'medium',
        'requires_approval': True,
        'penalty': 0.15,
        'description': 'Reassign to different agent or team'
    },
    'contact_customer': {
        'risk_tier': 'high',
        'requires_approval': True,
        'penalty': 0.20,
        'description': 'Proactively reach out to customer'
    },
    'flag_stale_ticket': {
        'risk_tier': 'low',
        'requires_approval': False,
        'penalty': 0.00,
        'description': 'Mark ticket for review'
    },
    # ... 5 more actions
}
```

**Approval Workflow:**

```python
def determine_approval_requirement(confidence, risk_tier):
    """
    Map confidence and risk to approval decision.
    
    Decision Matrix:
                    Low Risk  |  Medium Risk  |  High Risk
    High Conf (>78%)   Auto      Approval       Approval
    Med Conf (62-78%)  Auto      Approval       Approval
    Low Conf (<62%)    Skip      Skip           Skip
    
    Returns: 'auto', 'approval_required', or 'skip'
    """
    if confidence < 0.62:
        return 'skip'  # too uncertain
    
    if risk_tier == 'low':
        return 'auto'  # low risk, execute immediately
    
    return 'approval_required'  # medium/high risk needs human
```

**Audit Trail:**
```python
approval_log = {
    'proposal_id': 'P-12345-escalate',
    'ticket_id': 'TKT-105878',
    'action_type': 'escalate_to_supervisor_queue',
    'confidence': 0.704,
    'rationale': 'Ticket at 97% SLA with angry customer...',
    'timestamp': '2024-01-02 23:19:00',
    'human_decision': 'approved',  # or 'modified' or 'rejected'
    'decision_time': '2024-01-02 23:20:15',
    'agent_notes': 'High-value account, good call'
}
```

---

### Learning Loop

**Purpose:** Iteratively improve confidence calibration based on human feedback

**v1.0 → v2.0 Calibration:**

```python
# v1.0 Results
approval_rate_v1 = 0.55  # Too low (too noisy)
modification_rate_v1 = 0.40  # Too high (directionally right but needs tuning)
rejection_rate_v1 = 0.05  # Acceptable

# Insights from v1.0
# - Action penalties too low (over-recommending high-disruption actions)
# - LLM confidence not weighted enough (overconfident)
# - Threshold for "modify" tier too narrow

# v2.0 Changes
ACTION_PENALTY['reassign_ticket'] = 0.15  # increased from 0.10
ACTION_PENALTY['contact_customer'] = 0.20  # increased from 0.15
LLM_CONFIDENCE_MULTIPLIER = 0.8 + (0.2 * llm_confidence)  # added multiplier
MODIFY_THRESHOLD = (0.62, 0.78)  # widened from (0.65, 0.75)

# v2.0 Results
approval_rate_v2 = 0.72  # Production-ready! ✓
modification_rate_v2 = 0.25  # Improved
rejection_rate_v2 = 0.025  # Very low (good)
```

**Feedback Integration:**
```python
def update_confidence_model(approval_history):
    """
    Learn from human decisions to improve future predictions.
    
    Tracks:
    - Which actions get approved vs rejected
    - Confidence levels that correlate with approval
    - Patterns in modifications (what humans change)
    """
    # Analyze approval patterns
    approved = approval_history[approval_history.decision == 'approved']
    rejected = approval_history[approval_history.decision == 'rejected']
    
    # Identify confidence thresholds
    approve_threshold = approved['confidence'].quantile(0.20)
    reject_threshold = rejected['confidence'].quantile(0.80)
    
    # Adjust action penalties based on rejection patterns
    for action in ACTION_CATALOG:
        action_rejections = rejected[rejected.action == action]
        if len(action_rejections) > 10:  # sufficient sample
            penalty_adjustment = 0.05  # increase penalty
            ACTION_CATALOG[action]['penalty'] += penalty_adjustment
```

---

## Data Flow

```
1. Ticket Created
   └→ Event: created (t=0)
   
2. Event Processor
   └→ Calculate elapsed_hours, remaining_hours
   
3. Risk Detector
   └→ If remaining < 30% of SLA: FLAG as intervention_candidate
   
4. Hybrid Confidence Engine
   ├→ Rules: urgency = 1 - (remaining / target)
   ├→ LLM: classify ticket → urgency_score
   └→ Fusion: (0.6 × rules) + (0.4 × LLM) - penalty
   
5. Action Selector
   └→ Match ticket context → recommended_action
   
6. Governance Check
   ├→ Low risk: Execute immediately
   └→ Med/High risk: Queue for human approval
   
7. Human Decision
   ├→ Approved: Execute → Log success → Learn
   ├→ Modified: Adjust → Execute → Log → Learn
   └→ Rejected: Cancel → Log → Learn (adjust confidence)
   
8. Learning Loop
   └→ Update confidence model for next iteration
```

---

## Performance Characteristics

### Latency

| Component | Latency | Notes |
|-----------|---------|-------|
| Event processing | <10ms | Pure Python, vectorized |
| Risk detection | <50ms | Simple threshold logic |
| Rules engine | <1ms | Deterministic calculation |
| LLM classification | ~2-3s | API call to GPT-4 |
| Hybrid fusion | <5ms | Weighted arithmetic |
| Action selection | <10ms | Catalog lookup |
| **Total per ticket** | **~2-3s** | LLM is bottleneck |

### Throughput

- **Sequential:** ~20 tickets/minute (LLM bound)
- **Parallel (10 workers):** ~200 tickets/minute
- **Batch processing:** 20,000 tickets in ~2 hours

### Cost

- **LLM API calls:** $0.0024 per classification
- **20,000 tickets:** ~$48 one-time
- **Monthly (180 interventions):** ~$13/month
- **Annual infrastructure:** ~$8,400 total

---

## Scalability Considerations

### Current (Portfolio Demo)
- Batch processing of historical data
- Single-threaded execution
- Local file storage

### Production Deployment
- **Event streaming:** Kafka/Redis for real-time events
- **Parallel processing:** Ray/Celery for distributed workers
- **Caching:** Redis for LLM response cache
- **Database:** PostgreSQL for tickets, TimescaleDB for events
- **API:** FastAPI for REST endpoints
- **Monitoring:** Prometheus + Grafana for metrics

**Estimated production capacity:** 10,000 tickets/day with 3-5 second latency

---

## Security & Privacy

- **API keys:** Stored in environment variables, never committed
- **Data anonymization:** No PII in logs or outputs
- **Audit trails:** All actions logged with timestamps and rationale
- **Access control:** Human approval required for sensitive actions
- **Rate limiting:** Prevents abuse of LLM API

---

## Testing Strategy

### Unit Tests
- Confidence calculation edge cases
- Risk level classification
- Action eligibility logic

### Integration Tests
- End-to-end ticket → intervention flow
- LLM integration (with mocking)
- Approval workflow simulation

### Performance Tests
- Latency benchmarks
- Throughput under load
- Memory profiling

---

## Future Architecture Enhancements

1. **Reinforcement Learning**
   - Learn optimal action selection from outcomes
   - A/B test different confidence thresholds

2. **Multi-Agent Orchestration**
   - Specialized agents for different ticket types
   - Agent coordination and handoff protocols

3. **Vector Database**
   - Similar ticket search (Pinecone/Weaviate)
   - Historical pattern matching

4. **Real-Time Streaming**
   - Kafka event bus
   - WebSocket dashboard updates

5. **Advanced Monitoring**
   - Drift detection (approval rates declining)
   - Model performance tracking
   - Alerting on anomalies

---

## References

- [Event-Driven Architecture](https://martinfowler.com/articles/201701-event-driven.html)
- [Human-in-the-Loop ML](https://arxiv.org/abs/2108.00941)
- [Enterprise AI Governance](https://www.mckinsey.com/capabilities/quantumblack/our-insights/getting-to-know-and-manage-your-biggest-ai-risks)

---

**Last Updated:** February 2026
