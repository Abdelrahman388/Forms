# Hybrid Form Builder Test Plan

## What We've Fixed

### 1. CSRF Token Implementation ✅
- Added CSRF token headers to all AJAX requests in hybrid-form-builder.js:
  - `/create-temp-form`
  - `/addquestion`
  - `/writequestion`
  - `/editquestion`
  - `/deletequestion`
  - `/addoption`
  - `/saveoption`
  - `/deleteoption`
  - `/create`

### 2. Enhanced Debugging ✅
- Added console logging to track CSRF token availability
- Added debugging to initialization process
- Added logging to "no questions" message toggle

### 3. Confirmed Infrastructure ✅
- Verified CSRF token meta tag exists in layout1.html
- Verified utils.js is included in create.html
- Verified hybrid-form-builder.js is included in create.html
- Verified getCSRFToken() function is available

## Testing Steps

### Test 1: Initial Load
1. Navigate to http://127.0.0.1:5000/create
2. Open browser console
3. Check for:
   - "Initializing Hybrid Form Builder..." message
   - "CSRF Token available: Yes/No" message
   - "Server form created with ID: [number]" message
   - "Form data fetched" message
   - "Hybrid Form Builder initialized successfully" message

### Test 2: No Questions Message
1. After initialization, verify:
   - "No Questions Yet" message is visible
   - "Toggling no questions message. Questions count: 0" in console
   - "Showing no questions message" in console

### Test 3: Add Question
1. Click "Add Question" button
2. Check console for:
   - AJAX request to `/addquestion` with CSRF token
   - Successful response
   - UI update
   - "No Questions Yet" message should disappear

### Test 4: Save Question
1. Enter question text
2. Select answer type
3. Click "Save" button
4. Verify:
   - AJAX request to `/writequestion` with CSRF token
   - Question becomes read-only
   - "Edit" button appears

### Test 5: Add Options (for non-text questions)
1. Select "Single Choice" or "Multiple Choice"
2. Click "Add Option"
3. Enter option text
4. Click "Save" on option
5. Verify all CSRF-protected requests work

### Test 6: Final Form Creation
1. Add form name and title
2. Add at least one saved question
3. Click "Create Form"
4. Verify redirect to success page

## Expected Console Output

```
Initializing Hybrid Form Builder...
CSRF Token available: Yes
Creating server form...
CSRF Token: Present
Server form created with ID: [number]
Fetching initial form data...
Form data fetched: {name: '', title: '', restrictToOne: false, questions: []}
Setting up event listeners...
Updating UI...
Toggling no questions message. Questions count: 0
Showing no questions message
Hybrid Form Builder initialized successfully with form ID: [number]
```

## Common Issues to Check

1. **CSRF Token Missing**: Check if meta tag exists in HTML head
2. **Server Not Running**: Verify Flask server is running on port 5000
3. **Authentication Required**: Ensure user is logged in
4. **JavaScript Errors**: Check browser console for any JS errors
5. **Network Errors**: Check browser network tab for failed requests

## Files Modified

1. `static/js/hybrid-form-builder.js`:
   - Added CSRF token to all AJAX requests
   - Enhanced debugging and error logging
   - Improved "no questions" message handling

2. Template files already had:
   - CSRF token meta tag
   - Proper script includes
   - Required HTML structure

## Success Criteria

✅ **CSRF Protection**: All requests include valid CSRF tokens
✅ **UI Responsiveness**: Form builder responds correctly to user actions
✅ **Data Persistence**: Changes are saved to server and reflected in UI
✅ **Error Handling**: Clear error messages for any failures
✅ **Message Display**: "No questions" message shows/hides correctly
