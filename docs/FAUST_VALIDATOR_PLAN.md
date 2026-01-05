# FAUST Validator System - Implementation Plan

## Problem
LLMs don't understand FAUST. RAG doesn't fix this. We need a validation layer that actually knows the rules.

## Solution
```
User → AI (first draft) → Python Validator → Clean errors → AI retries → Valid code → Compiler
```

---

## Phase 1: The Bible (faust_bible.json)

**Goal:** Parse all faustlibraries and extract every valid function.

**Steps:**
1. Clone faustlibraries: `git clone https://github.com/grame-cncm/faustlibraries`
2. Parse all .lib files
3. Extract for each function:
   - Name and prefix (e.g., `fi.lowpass`)
   - Argument count and names
   - Input/output count
   - Description/gotchas from comments
4. Output: `static/faust_bible.json`

**Example output:**
```json
{
  "fi.lowpass": {
    "prefix": "fi",
    "name": "lowpass",
    "args": ["order", "cutoff"],
    "inputs": 1,
    "outputs": 1,
    "description": "Nth order Butterworth lowpass filter"
  },
  "en.adsr": {
    "prefix": "en",
    "name": "adsr",
    "args": ["attack", "decay", "sustain", "release", "gate"],
    "inputs": 0,
    "outputs": 1,
    "description": "ADSR envelope generator, gate triggers attack"
  }
}
```

---

## Phase 2: Error Catalog (error_catalog.json)

**Goal:** Extract every FAUST compiler error and map to actionable fixes.

**Steps:**
1. Clone FAUST: `git clone https://github.com/grame-cncm/faust`
2. Grep for error patterns in `compiler/**/*.cpp`
3. Map each error to:
   - Pattern (regex)
   - Cause
   - Fix suggestion

**Example output:**
```json
{
  "endless_evaluation_cycle": {
    "pattern": "endless evaluation cycle of \\d+ steps",
    "cause": "Recursive definition - variable references itself",
    "fix": "Rename variable to avoid conflict with library prefix. Use 'env' not 'envelope', 'lpf' not 'filter'."
  },
  "input_output_mismatch": {
    "pattern": "inputs/outputs mismatch",
    "cause": "Signal routing error - output count doesn't match next stage input",
    "fix": "Check : and , operators. Use <: to split, :> to merge."
  }
}
```

---

## Phase 3: Validator Core

### 3.1 Syntax Checker
- Tokenize FAUST code
- Check all function calls against faust_bible.json
- Flag unknown functions, wrong arg counts

### 3.2 Signal Flow Analyzer
- Parse code into simple AST
- Track input/output counts through `:`, `,`, `<:`, `:>`, `~`
- Catch routing mismatches before compiler

### 3.3 Semantic Checker
- Pattern match known traps:
  - `ba.if` with divide-by-zero in both branches (strict evaluation)
  - Recursive definitions (variable = variable.something)
  - String assignments to variables

### 3.4 Error Translator
- Take raw compiler error
- Match against error_catalog.json
- Return actionable message

---

## Phase 4: Grammar Constraint (Optional, Advanced)

**Goal:** Constrain LLM generation to only produce valid FAUST syntax.

**Requires:** Switch from Ollama to llama-cpp-python (supports GBNF grammar)

**Steps:**
1. Generate GBNF grammar from faust_bible.json
2. Use grammar-constrained generation
3. LLM can only output valid function names

**Trade-off:** More complex setup, but prevents hallucinated functions entirely.

---

## Phase 5: Integration

### 5.1 Validation API
```python
from faust_validator import validate

result = validate(code)
# result.valid: bool
# result.errors: List[ValidationError]
# result.warnings: List[str]

for err in result.errors:
    print(f"Line {err.line}: {err.message}")
    print(f"Fix: {err.suggestion}")
```

### 5.2 Auto-Retry Loop
```python
def generate_faust_with_validation(prompt, max_attempts=3):
    for attempt in range(max_attempts):
        code = llm.generate(prompt)
        result = validate(code)

        if result.valid:
            return code

        # Feed errors back to LLM
        prompt = f"""
        Previous attempt had errors:
        {result.errors}

        Fix the code:
        {code}
        """

    return None  # Failed after max attempts
```

### 5.3 UI Integration
- Add validation step in editor_ui.py
- Show validation errors before running compiler
- Color-code: validation errors (yellow), compiler errors (red)

---

## File Structure

```
src/faust_validator/
├── static/
│   ├── faust_bible.json      # All valid functions
│   ├── error_catalog.json    # Error→fix mappings
│   └── faust.gbnf            # Optional grammar
├── core/
│   ├── bible_parser.py       # Parse .lib files
│   ├── syntax_checker.py     # Check function calls
│   ├── signal_analyzer.py    # Track I/O routing
│   ├── semantic_checker.py   # Known traps
│   └── error_translator.py   # Compiler error→actionable
├── validator.py              # Main interface
└── __init__.py
```

---

## Priority Order

1. **Phase 1 + 2** - Get the data (Bible + Error catalog)
2. **Phase 3.4** - Error translator (immediate value)
3. **Phase 3.1** - Syntax checker (catch unknown functions)
4. **Phase 3.3** - Semantic checker (catch known traps)
5. **Phase 3.2** - Signal analyzer (harder, more value)
6. **Phase 5** - Integration
7. **Phase 4** - Grammar constraint (optional, advanced)

---

## Success Metrics

- [ ] Parse 100% of faustlibraries functions
- [ ] Catalog 100% of compiler error patterns
- [ ] Catch 80%+ of errors before compiler runs
- [ ] All error messages include actionable fix suggestions
- [ ] Auto-retry produces valid code in ≤3 attempts for common tasks

---

## Resources Needed

- faustlibraries repo: https://github.com/grame-cncm/faustlibraries
- faust compiler repo: https://github.com/grame-cncm/faust
- Existing FAUST docs in ChromaDB (for context)
