# JavaScript Modules Structure

The main.js file has been split into modular components for better maintainability and organization.

## Module Structure

### Core Modules

#### 1. `utils.js` - Utility Functions
- **Purpose**: Common functionality used across all modules
- **Exports**: `FormsUtils` namespace
- **Functions**:
  - `getCSRFToken()` - Retrieve CSRF token for AJAX requests
  - `showError(message)` - Display error messages to users
  - `showSuccess(message)` - Display success messages to users
  - `makeRequest(url, options)` - Make AJAX requests with CSRF protection

#### 2. `theme.js` - Theme Management
- **Purpose**: Handle dark/light mode toggle functionality
- **Exports**: `ThemeManager` namespace
- **Functions**:
  - `initializeThemeToggle()` - Set up theme toggle button
  - `toggleTheme()` - Switch between dark and light themes

#### 3. `form-builder.js` - Form Creation
- **Purpose**: Handle form and question management
- **Exports**: `FormBuilder` namespace
- **Functions**:
  - `initializeFormBuilder()` - Initialize all form builder functionality
  - `addQuestion(formId)` - Add new question to form
  - `deleteQuestion(questionId, formId)` - Remove question from form
  - `editQuestion(questionId, formId)` - Edit existing question
  - `saveQuestion(questionId)` - Save question changes
  - `updateQuestion(questionId, answerType, questionText)` - Update question properties
  - `updateQuestionType(question, answerType)` - Change question type and UI
  - `submitForm()` - Submit complete form
  - `deleteForm(formId)` - Delete entire form

#### 4. `option-manager.js` - Option Management
- **Purpose**: Handle question options (radio buttons, checkboxes)
- **Exports**: `OptionManager` namespace
- **Functions**:
  - `initializeOptionManagement()` - Set up option management events
  - `addOption(questionId, formId, answerType)` - Add new option to question
  - `saveOption(optionId, questionId)` - Save option changes (legacy)
  - `saveOptionText(optionId, questionId, optionText)` - Save option with text
  - `deleteOption(optionId, questionId)` - Remove option from question

#### 5. `response-manager.js` - Form Responses
- **Purpose**: Handle form submission by end users
- **Exports**: `ResponseManager` namespace
- **Functions**:
  - `initializeResponseForm()` - Set up response form events
  - `submitResponse()` - Submit form response data

#### 6. `charts.js` - Data Visualization
- **Purpose**: Create charts for response analytics
- **Exports**: `ChartsManager` namespace
- **Functions**:
  - `initializeCharts()` - Initialize charts on statistics page
  - `renderCharts(questions, optionCounts)` - Render multiple charts
  - `createChart(containerId, question, optionData)` - Create single chart

#### 7. `main.js` - Application Coordinator
- **Purpose**: Initialize and coordinate all modules
- **Functions**:
  - `initializeApplication()` - Start all modules
  - Global compatibility functions for onclick handlers

## Loading Order

The modules should be loaded in this order in your HTML templates:

```html
<!-- Core utilities first -->
<script src="{{ url_for('static', filename='js/utils.js') }}"></script>

<!-- Individual modules -->
<script src="{{ url_for('static', filename='js/theme.js') }}"></script>
<script src="{{ url_for('static', filename='js/form-builder.js') }}"></script>
<script src="{{ url_for('static', filename='js/option-manager.js') }}"></script>
<script src="{{ url_for('static', filename='js/response-manager.js') }}"></script>
<script src="{{ url_for('static', filename='js/charts.js') }}"></script>

<!-- Main coordinator last -->
<script src="{{ url_for('static', filename='js/main.js') }}"></script>
```

## Backward Compatibility

The new modular structure maintains full backward compatibility with existing HTML templates that use onclick handlers. The following global functions are still available:

### Form Builder Functions
- `addQuestion(formId)`
- `deleteQuestion(questionId, formId)`
- `editQuestion(questionId, formId)`
- `saveQuestion(questionId)`
- `updateQuestion(questionId, answerType, questionText)`

### Option Management Functions
- `addOption(questionId, formId, answerType)`
- `saveOption(optionId, questionId)`
- `deleteOption(optionId, questionId)`

### Utility Functions
- `getCSRFToken()`
- `showError(message)`
- `showSuccess(message)`

## Benefits of Modular Structure

1. **Maintainability**: Each module handles a specific concern
2. **Reusability**: Modules can be imported independently
3. **Testing**: Individual modules can be tested in isolation
4. **Performance**: Only load required modules per page
5. **Debugging**: Easier to locate and fix issues
6. **Team Development**: Multiple developers can work on different modules

## Module Dependencies

```
main.js
├── utils.js (required by all other modules)
├── theme.js → utils.js
├── form-builder.js → utils.js
├── option-manager.js → utils.js
├── response-manager.js → utils.js
└── charts.js → utils.js
```

## Adding New Modules

To add a new module:

1. Create the new `.js` file in `static/js/`
2. Follow the namespace pattern: `window.ModuleName = { ... }`
3. Use `FormsUtils` for common operations
4. Add initialization call in `main.js`
5. Add script tag to templates
6. Document the module in this guide

## File Sizes (Approximate)

- `utils.js`: ~3KB
- `theme.js`: ~1KB
- `form-builder.js`: ~8KB
- `option-manager.js`: ~4KB
- `response-manager.js`: ~2KB
- `charts.js`: ~3KB
- `main.js`: ~2KB

**Total**: ~23KB (vs. original 30KB monolithic file)

## Migration Notes

- ✅ Original `main.js` backed up as `tests/main-original.js`
- ✅ All functionality preserved
- ✅ No template changes required
- ✅ Backward compatible onclick handlers
- ✅ Improved error handling with `FormsUtils.showError()`
- ✅ Consistent AJAX requests with `FormsUtils.makeRequest()`
