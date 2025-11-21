# CLAUDE.md - AI Assistant Guide for Welcome Letter Generator

## Project Overview

**Welcome Letter Generator** is a single-page web application designed to generate personalized IT onboarding welcome letters for new employees across multiple companies (T1ES, T1CS, CCSU, DefOpt). The application creates two versions of each letter:
1. **User version** - Contains a secure PWPush link that expires
2. **Manager copy** - Contains the plaintext password for internal records

### Purpose
Streamline IT onboarding by automatically generating standardized welcome letters containing:
- Employee credentials (username, email, password)
- Computer assignment details
- Network access information
- Support contact information
- Company-specific branding

## Repository Structure

```
welcomeLetterGen/
├── welcomeLetterGenerator.html  # Main application (single-file SPA)
├── password_generator.py        # Standalone Python module for password generation
├── LICENSE                      # MIT License
└── .git/                        # Git repository
```

### File Responsibilities

#### `welcomeLetterGenerator.html` (622 lines)
- **Primary application file** - Self-contained HTML/CSS/JavaScript SPA
- **No external dependencies** - All logic embedded in single file
- Contains:
  - User interface with dark theme styling
  - Form validation logic
  - Password generation algorithm (JavaScript implementation)
  - Welcome letter HTML template
  - PWPush API integration
  - Window/popup management

#### `password_generator.py` (85 lines)
- **Standalone Python module** extracted from JavaScript implementation
- Purpose: Server-side or CLI password generation
- Provides identical password format to HTML version
- Can be imported as module or run standalone
- Contains comprehensive docstrings and examples

## Development Workflow

### Git Branch Strategy

**CRITICAL**: All development occurs on feature branches with specific naming convention:
- Branch pattern: `claude/claude-md-{session-id}`
- Current branch: `claude/claude-md-mi8aete90dhsgl2w-018dTZ5RGmt84wE7rmHttL5Q`
- **Never push to main/master directly**
- All changes go through Pull Requests

### Commit Practices

Based on git history analysis:
1. **Use descriptive commit messages**
   - Example: "Add validation tooltip for middle names (more than 2 words)"
   - Example: "Extract password generation logic to standalone Python module"
2. **One logical change per commit**
3. **Reference PR numbers in merge commits**
4. **Follow conventional commit style** (implied from history)

### Pull Request Workflow

1. Create feature branch with `claude/` prefix
2. Make changes and commit with clear messages
3. Push to origin: `git push -u origin <branch-name>`
4. Create PR via GitHub interface (gh CLI not available)
5. Merge after review

## Key Conventions & Rules

### Name Validation Rules (CRITICAL)

The application enforces strict name validation with real-time feedback:

1. **Exactly 2 words required**
   - MUST have first name AND last name
   - NO middle names allowed
   - Validation error: "Middle names not allowed - only first and last name"
   - Location: `welcomeLetterGenerator.html:191-198`

2. **Combined character limit: 19 characters**
   - firstName.length + lastName.length ≤ 19
   - Real-time validation as user types
   - Location: `welcomeLetterGenerator.html:203-211`

3. **Distinct names required**
   - First and last name must be different words
   - Case-insensitive comparison
   - Location: `welcomeLetterGenerator.html:516-519`

4. **Validation triggers**
   - `oninput`: Real-time validation during typing
   - `onblur`: Single-word validation when field loses focus
   - `onfocus`: Clears error tooltips when field gains focus

### Password Generation

**Format**: `word-WORD-word-##`

**Components**:
- First word: lowercase (from wordlist)
- Second word: UPPERCASE (from wordlist)
- Third word: lowercase (from wordlist)
- Two-digit number: 10-99 (random)

**Example**: `alpha-STORM-river-42`

**Wordlist** (56 words):
- Categories: Greek letters, weather, nature, animals, tech/sci-fi terms
- Location: `welcomeLetterGenerator.html:258-266` (JavaScript)
- Location: `password_generator.py:13-21` (Python)

**Implementation locations**:
- JavaScript: `generatePassword()` at line 454-457
- Python: `generate_password()` at line 24-52

### Company Configuration

Four companies supported with specific configurations:

| Company | Code   | Email Domain              | Logo URL                                    |
|---------|--------|---------------------------|---------------------------------------------|
| Tier 1 Energy Solutions | T1ES | @tier1energy.ca | cdn.prod.website-files.com/5e59748a... |
| Tier 1 Competitions Solutions | T1CS | @tier1cs.com | cdn.prod.website-files.com/5e6ff5d2... |
| Canatex Completion Solutions | CCSU | @canatexcompletions.com | cdn.prod.website-files.com/59a43992... |
| Definitive Optimization | DefOpt | @defopt.com | defopt.com/images/logo_definitive... |

**Configuration locations**:
- Email domains: `welcomeLetterGenerator.html:277-282`
- Logo URLs: `welcomeLetterGenerator.html:269-274`

### Computer Naming Convention

- Format: `TIER1LP###` (3-digit zero-padded number)
- Example: `TIER1LP001`, `TIER1LP555`
- If no computer number provided: Display `___` as placeholder
- Location: `welcomeLetterGenerator.html:553`

### PWPush Integration

**Purpose**: Secure password delivery with automatic expiration

**API Endpoint**: `https://pwpush.com/p.json`

**Expiry Calculation**:
```javascript
expiryDays = (daysUntilStart + 7)
minimum = 7 days
```

**Parameters**:
- `expire_after_days`: Calculated based on start date
- `expire_after_views`: 20 views maximum
- Location: `welcomeLetterGenerator.html:459-473`

**Return format**: `https://pwpush.com/p/{url_token}`

### Date Handling

1. **Start date is optional**
   - If blank: Uses current date
   - If provided: Must not be in past
2. **Date validation only if user provides date**
   - Location: `welcomeLetterGenerator.html:534-543`
3. **Minimum date**: Today (enforced in HTML input)
   - Location: `welcomeLetterGenerator.html:171`

## User Interface Patterns

### Error Display Strategy

**Three types of error tooltips**:

1. **nameLengthError** - Combined name > 19 characters
   - Shows during typing (`oninput`)
   - Red border on input
   - Location: `welcomeLetterGenerator.html:146`

2. **singleWordError** - Only one word entered
   - Shows on blur (field loses focus)
   - Hidden on focus
   - Location: `welcomeLetterGenerator.html:147`

3. **middleNameError** - More than 2 words entered
   - Shows during typing (`oninput`)
   - Red border on input
   - Location: `welcomeLetterGenerator.html:148`

### Status Messages

Three status types:
- `.success` - Green background, operations completed
- `.error` - Red background, validation or runtime errors
- `.info` - Blue background, progress updates

Location: `welcomeLetterGenerator.html:90-104`

### Dark Theme

- Background: `#1e1e1e`
- Container: `#2d2d2d`
- Primary color: `#0078d4` (Microsoft blue)
- Success color: `#28a745`
- All colors use dark mode palette

## Code Patterns to Follow

### 1. Input Validation Pattern

```javascript
// Always validate on multiple events
<input
    oninput="validateNameLength()"    // Real-time validation
    onblur="validateFullNameOnBlur()" // On field exit
    onfocus="clearSingleWordError()"  // On field entry
>
```

### 2. Error Display Pattern

```javascript
function showError(tooltipId, inputId) {
    document.getElementById(tooltipId).classList.add('show');
    document.getElementById(inputId).classList.add('error');
}

function hideError(tooltipId, inputId) {
    document.getElementById(tooltipId).classList.remove('show');
    document.getElementById(inputId).classList.remove('error');
}
```

### 3. Status Message Pattern

```javascript
function showStatus(message, type) {
    const status = document.getElementById('status');
    status.textContent = message;
    status.className = `status ${type} show`;
}
```

### 4. Window Management

**Important**: Sequential opening to avoid popup blockers
```javascript
// Open first window immediately
const win1 = window.open('', '_blank');
win1.document.write(htmlContent);

// Delay second window by 1 second
setTimeout(() => {
    const win2 = window.open('', '_blank');
    win2.document.write(htmlContent);
}, 1000);
```

Location: `welcomeLetterGenerator.html:572-614`

### 5. Async/Await Pattern for API Calls

```javascript
async function generateLetters() {
    try {
        const pwpushLink = await createPwPushLink(password, expiryDays);
        // Continue with link...
    } catch (error) {
        showStatus('Error: ' + error.message, 'error');
    }
}
```

## Testing Considerations

### Manual Testing Checklist

When modifying validation or generation logic, test:

1. **Name validation**:
   - [ ] Single word (should error on blur)
   - [ ] Two words with combined length = 19 (should pass)
   - [ ] Two words with combined length = 20 (should error)
   - [ ] Three words (should error immediately)
   - [ ] Same first and last name (should error)

2. **Password generation**:
   - [ ] Auto-generated follows pattern: `word-WORD-word-##`
   - [ ] Custom password is used when provided
   - [ ] Password appears in both documents

3. **Date handling**:
   - [ ] Blank date uses today
   - [ ] Past date shows error
   - [ ] Future date calculates correct expiry

4. **Company selection**:
   - [ ] Correct logo appears for each company
   - [ ] Correct email domain for each company

5. **Computer number**:
   - [ ] Blank shows `___`
   - [ ] Number formats correctly (zero-padded to 3 digits)

6. **Popup behavior**:
   - [ ] Both windows open successfully
   - [ ] Correct titles on each window
   - [ ] Copy button functions correctly

## Common Modification Scenarios

### Adding a New Company

1. Add to company dropdown (line 129-134)
2. Add logo URL to `logoUrls` object (line 269-274)
3. Add email domain to `emailDomains` object (line 277-282)

### Modifying Name Length Limit

Current limit: 19 characters (first + last combined)

To change:
1. Update validation in `validateNameLength()` (line 205)
2. Update error message (line 146)
3. Update validation in `generateLetters()` (line 523)
4. Update error message in `generateLetters()` (line 524)

### Changing Password Format

**Locations to update**:
1. JavaScript: `generatePassword()` (line 454-457)
2. Python: `generate_password()` (password_generator.py:24-52)
3. Update wordlist if needed (both files)
4. Update documentation/comments

### Modifying PWPush Expiry Logic

Current formula: `(daysUntilStart + 7)` with minimum 7 days

Location: `calculateExpiryDays()` at line 439-452

## Security Considerations

### Implemented Security Measures

1. **Password expiration** - PWPush links auto-expire
2. **View limits** - 20 views maximum per password link
3. **No password storage** - Passwords never stored server-side
4. **HTTPS enforcement** - PWPush API uses HTTPS
5. **Client-side generation** - No passwords transmitted during generation

### Security Notes for AI Assistants

- **Never log passwords** in console or error messages
- **Never commit passwords** to repository
- **Validate all user input** before processing
- **Handle API failures gracefully** without exposing sensitive data
- **Respect popup blockers** - they're a security feature

## Dependencies & External Services

### External APIs

1. **PWPush** (`https://pwpush.com`)
   - Purpose: Secure password link generation
   - No API key required
   - Rate limits: Unknown (use responsibly)

### External Resources

1. **Company logos** - Hosted on CDN (cdn.prod.website-files.com)
2. **Yardstick Technologies logo** - Hosted on johncameron.com
3. **YouTube tutorial** - Embedded link in generated letters

### No External JavaScript Libraries

- **Pure vanilla JavaScript** - No jQuery, React, etc.
- **No build process required** - Direct HTML file execution
- **No package.json** - Zero npm dependencies

## File Modification Guidelines

### When to Edit `welcomeLetterGenerator.html`

- Adding/modifying validation rules
- Changing UI/styling
- Updating company configurations
- Modifying letter template
- Changing password generation logic

### When to Edit `password_generator.py`

- Need server-side password generation
- Creating CLI tools
- Batch password generation
- **Must keep in sync** with JavaScript implementation

### Keeping Implementations in Sync

The password generation logic exists in two places:

**JavaScript** (welcomeLetterGenerator.html:454-457):
```javascript
function generatePassword() {
    const r = () => wordlist[Math.floor(Math.random() * wordlist.length)];
    return `${r().toLowerCase()}-${r().toUpperCase()}-${r().toLowerCase()}-${Math.floor(Math.random() * 90) + 10}`;
}
```

**Python** (password_generator.py:24-52):
```python
def generate_password():
    random_word = lambda: random.choice(WORDLIST)
    word1 = random_word().lower()
    word2 = random_word().upper()
    word3 = random_word().lower()
    number = random.randint(10, 99)
    password = f"{word1}-{word2}-{word3}-{number}"
    return password
```

**Rule**: Changes to wordlist or format MUST be applied to both files.

## HTML Letter Template

### Template Location
Embedded string literal at line 285-431

### Placeholders Used
- `FIRSTNAME` - Employee first name
- `LASTNAME` - Employee last name
- `USERLOGIN` - Format: `FirstName.LastName`
- `COMPUTERNAME` - Format: `TIER1LP###` or `___`
- `EMAILADDRESS` - Format: `FirstName.LastName@domain.com`
- `PASSWORDFIELD` - Either PWPush link or plaintext password
- `TIER1LOGOURL` - Company-specific logo URL

### Template Styling
- Font: Calibri, Arial, sans-serif
- Size: 11pt body, 12pt greeting
- Print-optimized with `@media print` rules
- Dual-logo header (Yardstick + Company)

## Debugging Tips

### Common Issues

1. **Popup blocked**
   - Check browser popup settings
   - User must allow popups for the site
   - Second window has 1-second delay to avoid blocker

2. **PWPush API failure**
   - Check network connectivity
   - Verify API endpoint is accessible
   - Check browser console for errors

3. **Name validation not working**
   - Check event handlers are attached
   - Verify tooltip IDs match JavaScript selectors
   - Check CSS classes for `.show` and `.error`

4. **Password format incorrect**
   - Verify wordlist is loaded
   - Check random number generation (10-99 range)
   - Ensure no duplicate words selected

### Browser Console Checks

```javascript
// Verify wordlist loaded
console.log(wordlist.length); // Should be 56

// Test password generation
console.log(generatePassword());

// Check email domain mapping
console.log(emailDomains);

// Check logo URL mapping
console.log(logoUrls);
```

## Python Module Usage

### As Imported Module

```python
from password_generator import generate_password, generate_multiple_passwords

# Generate single password
pwd = generate_password()
print(pwd)  # e.g., 'alpha-STORM-river-42'

# Generate multiple passwords
pwds = generate_multiple_passwords(10)
for p in pwds:
    print(p)
```

### As Standalone Script

```bash
python3 password_generator.py
```

Output:
```
Password Generator
==================================================

Single password:
  alpha-STORM-river-42

10 example passwords:
   1. frost-EAGLE-cipher-77
   2. shadow-QUANTUM-ocean-23
   ...
```

## Project History & Evolution

### Initial Implementation (Commit: 1319323)
- Single HTML file with core functionality
- Basic password generation
- Letter template creation

### Validation Enhancements (Commits: 71d34a3, e508472)
- Added distinct name validation
- Added 19-character limit validation

### User Experience Improvements (PRs #3, #4)
- Added single-word name tooltip
- Added middle name validation tooltip
- Enhanced real-time validation feedback

### Code Extraction (PR #5)
- Extracted Python module for password generation
- Enabled server-side/CLI usage
- Maintained parity with JavaScript implementation

## Future Considerations

### Potential Enhancements
1. Backend API for password generation (currently client-side only)
2. Database integration for user record keeping
3. Email sending integration (currently manual)
4. Batch user import (CSV/Excel)
5. Custom wordlist management UI
6. Password strength configuration
7. Audit log for generated letters

### Refactoring Opportunities
1. Extract CSS to separate file
2. Extract JavaScript to separate file
3. Add unit tests for validation logic
4. Add integration tests for PWPush API
5. Create build process for minification

## License

MIT License - See LICENSE file for full text

Copyright (c) 2025 Odysseus32

## Questions & Support

For questions about this codebase, refer to:
1. This CLAUDE.md file first
2. Code comments in `welcomeLetterGenerator.html`
3. Docstrings in `password_generator.py`
4. Git commit history for context on changes
5. Pull request descriptions for feature rationale

---

**Last Updated**: 2025-11-21
**Repository**: Odysseus32/welcomeLetterGen
**Current Branch**: claude/claude-md-mi8aete90dhsgl2w-018dTZ5RGmt84wE7rmHttL5Q
