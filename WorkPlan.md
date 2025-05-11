# Updated Work Plan

## English Section

### Architecture Overview

The new architecture will be layer-based, helping us organize code in a modular and maintainable way:

1. **Domain Layer**:
   * **Purpose:** This layer defines the core business logic of the application. It contains data models, main data processing functions, and business rules. This layer is independent of other layers, making it reusable.
   * **Files:**
      * `data_model.py`: Defines data structures and basic operations on them (loading, filtering, sorting, etc.).
      * `data_loader.py`: Responsible for loading data from various sources (CSV, Excel, etc.).
      * `data_filter.py`: Provides functions for filtering and sorting data.
      * `intent_parser.py`: Analyzes user queries to understand their intent and relevant columns.
      * `data_processing.py`: Contains functions for processing and analyzing data (calculating averages, generating graphs, etc.).

2. **Infrastructure Layer**:
   * **Purpose:** This layer handles supporting functions not directly related to business logic, such as logging, performance monitoring, data export, etc.
   * **Files:**
      * `logger.py`: Handles logging of system actions, errors, and other information.
      * `performance_monitor.py`: Monitors system performance (runtime, resource usage, etc.).
      * `export.py`: Responsible for exporting data in various formats (CSV, Excel, JSON, etc.).

3. **Service Layer**:
   * **Purpose:** This layer provides application-specific services, using the domain and infrastructure layers. It integrates various operations and presents a unified interface to higher layers.
   * **Files:**
      * `file_profile_service.py`: Provides a service for creating file profiles (metadata, statistics, etc.).
      * `analysis_service.py`: Provides a service for performing complex analyses on data.

4. **Data Access Layer**:
   * **Purpose:** This layer is responsible for accessing data sources (databases, files, etc.). It separates business logic from the implementation details of data access, allowing for changes in data sources without modifying the rest of the code.
   * **Files:**
      * `file_profile_repository.py`: Handles saving and retrieving file profiles.
      * `analysis_record_repository.py`: Handles saving and retrieving analysis records.
      * `database_handler.py`: Provides an interface for accessing the database.

5. **Common Layer**:
   * **Purpose:** This layer contains shared files and components used by multiple different layers. This can include shared data models, helper functions, etc.
   * **Files:**
      * `your_models.py`: (temporary name) Contains shared data models.

6. **Project Root**:
   * **Purpose:** Contains the main entry point for the application and the main configuration files.
   * **Files:**
      * `main.py`: Main entry point of the application.
      * `README.md`: Explanation file about the project.
      * `WorkPlan.md`: Project work plan.

7. **Presentation Layer**:
   * **Purpose:** This layer is responsible for presenting data to the user and receiving input from the user. It includes the graphical user interface (GUI) or any other interface.
   * **Files:**
      * `gui.py`: Graphical user interface of the application.

### Implementation Plan

#### 1. Database Infrastructure Setup (SQLite)

1.1. Database Schema Design:
   - Define required tables: file_profiles and analyses.
   - Determine columns for each table, including data types (TEXT, INTEGER, FLOAT, DATETIME).
   - Decide on PRIMARY KEY for each table.
   - Consider indexes for frequently searched columns (like file_path in file_profiles).
   - Action: Create detailed sketch of database schema (tables and columns).

1.2. Implement DatabaseHandler Class:
   - Create a class handling all interaction with SQLite database.
   - Functions for creating database connection.
   - Functions for executing SQL queries (SELECT, INSERT, UPDATE).
   - Function for closing the connection.
   - Action: Write basic code for DatabaseHandler class.

1.3. Create Tables in Database:
   - Use DatabaseHandler class to execute SQL commands creating file_profiles and analyses tables (according to planned schema).
   - Action: Write function in DatabaseHandler or separate script for table creation.

#### 2. FileProfile Module Development

2.1. Define FileProfile Class:
   - Create class representing a file profile.
   - Properties: file_path, column_names (list), column_types (list), basic_stats (dictionary), column_vectors (list or array).
   - Action: Write code for FileProfile class.

2.2. Function for Creating File Profile:
   - Develop function in FileProfileService that receives file path, analyzes it, and returns populated FileProfile object.
   - Function will include logic for identifying basic data types and calculating basic statistics.
   - Action: Write create_file_profile function in FileProfileService.

2.3. Function for Saving File Profile to Database:
   - Develop function in FileProfileRepository that receives FileProfile object and uses DatabaseHandler to save information in file_profiles table.
   - Need to serialize (e.g., to JSON) properties like column_names, column_types, basic_stats, and column_vectors before saving them as text fields.
   - Action: Write save_file_profile function in FileProfileRepository.

#### 3. AnalysisRecord Module Development

3.1. Define AnalysisRecord Class:
   - Create class representing a performed analysis record.
   - Properties: file_path, query, analysis_type, column_names, settings, results_path, timestamp.
   - Action: Write code for AnalysisRecord class.

3.2. Function for Saving Analysis Record to Database:
   - Develop function in AnalysisRecordRepository that receives details about performed analysis and uses DatabaseHandler to save new record in analyses table.
   - Here too, might need to serialize some properties.
   - Action: Write save_analysis_record function in AnalysisRecordRepository.

#### 4. Profile Comparison and Recommendation Logic Implementation

4.1. Function for Comparing File Profiles:
   - Develop function in FileProfileService that receives two FileProfile objects and returns similarity measure between them (e.g., based on cosine similarity of column name vectors and overlap in column name sets).
   - Action: Write compare_file_profiles function in FileProfileService.

4.2. Function for Retrieving Similar Profiles from Database:
   - Develop function in FileProfileService that receives FileProfile object of new file, retrieves all existing profiles from file_profiles table, and uses compare_file_profiles function to find similar profiles.
   - Action: Write get_similar_file_profiles function in FileProfileService.

4.3. Function for Retrieving Relevant Analyses for Similar File:
   - Develop function in AnalysisService that receives path of similar file and retrieves analysis records performed on it from analyses table.
   - Action: Write get_analyses_for_file function in AnalysisService.

4.4. Function for Creating Analysis Recommendations:
   - Develop function in AnalysisService that receives FileProfile object of current file and list of analyses performed on similar files.
   - Function will analyze previous analyses and suggest relevant analyses for current file based on existing column names.
   - Action: Write generate_analysis_recommendations function in AnalysisService.

#### 5. Integration with User Interface (GUI)

5.1. Display Recommendations in GUI:
   - Update GUI to receive list of analysis recommendations from AnalysisService.
   - Add UI elements to display recommendations (e.g., list).
   - Action: Modify code in gui.py to display recommendations.

5.2. Option to Run Recommended Analysis:
   - Add functionality in GUI allowing user to select recommendation and run it.
   - Pass relevant information (analysis type, columns) to DataProcessing.
   - Action: Add interactivity to recommendations in gui.py.

5.3. Display Analysis History (Optional):
   - Consider adding option for user to see history of analyses performed on similar files.
   - Action: (If relevant) Add UI elements to display history and functionality to retrieve this information from AnalysisService.

#### 6. Testing and Improvements

6.1. Unit Tests:
   - Write unit tests for each new function developed (profile creation, comparison, saving, retrieval, recommendation creation).
   - Action: Write test code.

6.2. Integration Tests:
   - Test that different modules work together properly (e.g., file loading, profile creation, and saving to database are performed correctly).
   - Action: Write test code.

6.3. User Testing:
   - Test with users to get feedback on usefulness and relevance of recommendations.
   - Action: Conduct testing round with users.

6.4. Improvements and Iteration:
   - Based on test results and feedback, make improvements to code, algorithms, and interface design.
   - Action: Repeat previous steps as needed.

### Project Structure

To organize code effectively, we'll divide it into directories by architectural layers:

```
├── main.py
├── README.md
├── WorkPlan.md
├── domain/
│   ├── data_model.py
│   ├── data_loader.py
│   ├── data_filter.py
│   ├── intent_parser.py
│   └── data_processing.py
├── infrastructure/
│   ├── logger.py
│   ├── performance_monitor.py
│   └── export.py
├── service/
│   ├── file_profile_service.py
│   └── analysis_service.py
├── data_access/
│   ├── file_profile_repository.py
│   ├── analysis_record_repository.py
│   └── database_handler.py
├── common/
│   └── your_models.py
├── presentation/
│   └── gui.py
└── logs/
```

### Progress Status

#### Completed:
- Defined new architecture
- Planned directory and file structure
- Basic FileProfile and AnalysisRecord classes exist (but need improvement)

#### Not Started:
- Development of new functionality (database work, service layer, comparison and recommendation logic)
- Writing tests

---

## Hebrew Section

### תוכנית העבודה המעודכנת

#### סקירת הארכיטקטורה

הארכיטקטורה החדשה תהיה מבוססת על שכבות, מה שיעזור לנו לארגן את הקוד בצורה מודולרית וקלה לתחזוקה:

1. **שכבת מודל הנתונים (Domain Layer)**:
   * **תפקיד:** שכבה זו מגדירה את הלוגיקה העסקית הבסיסית של האפליקציה. היא מכילה את המודלים של הנתונים, את הפונקציות העיקריות לטיפול בנתונים, ואת הכללים העסקיים. שכבה זו אינה תלויה בשכבות אחרות, ולכן היא ניתנת לשימוש חוזר.
   * **קבצים:**
      * `data_model.py`: מגדיר את מבנה הנתונים ואת הפעולות הבסיסיות עליהם (טעינה, סינון, מיון וכו').
      * `data_loader.py`: אחראי על טעינת הנתונים ממקורות שונים (CSV, Excel וכו').
      * `data_filter.py`: מספק פונקציות לסינון ומיון הנתונים.
      * `intent_parser.py`: מנתח את שאילתות המשתמש כדי להבין את הכוונה שלו ואת העמודות הרלוונטיות.
      * `data_processing.py`: מכיל פונקציות לעיבוד וניתוח הנתונים (חישוב ממוצעים, גרפים וכו').

2. **שכבת תשתיות (Infrastructure Layer)**:
   * **תפקיד:** שכבה זו מטפלת בפונקציות תומכות שאינן קשורות ישירות ללוגיקה העסקית, כמו רישום לוגים, ניטור ביצועים, ייצוא נתונים וכו'.
   * **קבצים:**
      * `logger.py`: מטפל ברישום לוגים של פעולות המערכת, שגיאות ומידע אחר.
      * `performance_monitor.py`: מנטר את ביצועי המערכת (זמן ריצה, שימוש במשאבים וכו').
      * `export.py`: אחראי על ייצוא הנתונים בפורמטים שונים (CSV, Excel, JSON וכו').

3. **שכבת שירות (Service Layer)**:
   * **תפקיד:** שכבה זו מספקת שירותים ספציפיים לאפליקציה, תוך שימוש בשכבות ה-domain וה-infrastructure. היא מתכללת את הפעולות השונות ומציגה ממשק אחיד לשכבות הגבוהות יותר.
   * **קבצים:**
      * `file_profile_service.py`: מספק שירות ליצירת פרופילים של קבצים (מטא-דאטה, סטטיסטיקות וכו').
      * `analysis_service.py`: מספק שירות לביצוע אנליזות מורכבות על הנתונים.

4. **שכבת גישה לנתונים (Data Access Layer)**:
   * **תפקיד:** שכבה זו אחראית על הגישה למקורות הנתונים (בסיסי נתונים, קבצים וכו'). היא מפרידה את הלוגיקה העסקית מפרטי היישום של הגישה לנתונים, כך שניתן להחליף את מקור הנתונים בלי לשנות את שאר הקוד.
   * **קבצים:**
      * `file_profile_repository.py`: מטפל בשמירה ואחזור של פרופילי קבצים.
      * `analysis_record_repository.py`: מטפל בשמירה ואחזור של רשומות אנליזה.
      * `database_handler.py`: מספק ממשק לגישה לבסיס הנתונים.

5. **שכבת קבצים משותפים (Common Layer)**:
   * **תפקיד:** שכבה זו מכילה קבצים ורכיבים משותפים שנעשה בהם שימוש על ידי מספר שכבות שונות. זה יכול לכלול מודלים של נתונים משותפים, פונקציות עזר וכו'.
   * **קבצים:**
      * `your_models.py`: (שם זמני) מכיל מודלים של נתונים משותפים.

6. **שורש הפרויקט**:
   * **תפקיד:** מכיל את נקודת הכניסה הראשית לאפליקציה ואת קבצי התצורה הראשיים.
   * **קבצים:**
      * `main.py`: נקודת הכניסה הראשית של האפליקציה.
      * `README.md`: קובץ הסבר על הפרויקט.
      * `WorkPlan.md`: תוכנית העבודה של הפרויקט.

7. **שכבת מצגת (Presentation Layer)**:
   * **תפקיד:** שכבה זו אחראית על הצגת הנתונים למשתמש ועל קבלת קלט מהמשתמש. היא כוללת את ממשק המשתמש הגרפי (GUI) או כל ממשק אחר.
   * **קבצים:**
      * `gui.py`: ממשק המשתמש הגרפי של האפליקציה.

### תוכנית ביצוע

#### 1. הקמת תשתית מסד הנתונים (SQLite)

1.1. תכנון סכמת מסד הנתונים:
   - הגדרת הטבלאות הדרושות: file_profiles ו-analyses.
   - קביעת העמודות עבור כל טבלה, כולל סוגי הנתונים (TEXT, INTEGER, FLOAT, DATETIME).
   - החלטה על מפתח ראשי (PRIMARY KEY) עבור כל טבלה.
   - שקילת אינדקסים עבור עמודות שיהיו בשימוש תדיר בחיפושים (כמו file_path ב-file_profiles).
   - פעולה: יצירת סקיצה מפורטת של סכמת מסד הנתונים (טבלאות ועמודות).

1.2. הטמעת מחלקת DatabaseHandler:
   - יצירת מחלקה שתטפל בכל האינטראקציה עם מסד הנתונים SQLite.
   - פונקציות ליצירת חיבור למסד הנתונים.
   - פונקציות לביצוע שאילתות SQL (SELECT, INSERT, UPDATE).
   - פונקציה לסגירת החיבור.
   - פעולה: כתיבת קוד בסיסי למחלקה DatabaseHandler.

1.3. יצירת טבלאות במסד הנתונים:
   - שימוש במחלקה DatabaseHandler כדי לבצע פקודות SQL ליצירת הטבלאות file_profiles ו-analyses (בהתאם לסכמה שתכננו).
   - פעולה: כתיבת פונקציה ב-DatabaseHandler או סקריפט נפרד ליצירת הטבלאות.

#### 2. פיתוח מודול FileProfile

2.1. הגדרת מחלקת FileProfile:
   - יצירת מחלקה שתייצג פרופיל של קובץ.
   - מאפיינים: file_path, column_names (רשימה), column_types (רשימה), basic_stats (מילון), column_vectors (רשימה או מערך).
   - פעולה: כתיבת קוד למחלקת FileProfile.

2.2. פונקציה ליצירת פרופיל קובץ:
   - פיתוח פונקציה ב-FileProfileService שתקבל נתיב לקובץ, תנתח אותו ותחזיר אובייקט FileProfile מאוכלס.
   - הפונקציה תכלול לוגיקה לזיהוי סוגי נתונים בסיסיים וחישוב סטטיסטיקות בסיסיות.
   - פעולה: כתיבת פונקציה create_file_profile ב-FileProfileService.

2.3. פונקציה לשמירת פרופיל קובץ במסד הנתונים:
   - פיתוח פונקציה ב-FileProfileRepository שתקבל אובייקט FileProfile ותשתמש ב-DatabaseHandler כדי לשמור את המידע בטבלת file_profiles.
   - יהיה צורך לבצע סדרתיות (למשל, ל-JSON) עבור מאפיינים כמו column_names, column_types, basic_stats ו-column_vectors לפני שמירתם כשדות טקסט.
   - פעולה: כתיבת פונקציה save_file_profile ב-FileProfileRepository.

#### 3. פיתוח מודול AnalysisRecord

3.1. הגדרת מחלקת AnalysisRecord:
   - יצירת מחלקה שתייצג רשומה של ניתוח שבוצע.
   - מאפיינים: file_path, query, analysis_type, column_names, settings, results_path, timestamp.
   - פעולה: כתיבת קוד למחלקת AnalysisRecord.

3.2. פונקציה לשמירת רשומת ניתוח במסד הנתונים:
   - פיתוח פונקציה ב-AnalysisRecordRepository שתקבל פרטים על ניתוח שבוצע ותשתמש ב-DatabaseHandler כדי לשמור רשומה חדשה בטבלת analyses.
   - גם כאן, ייתכן שנצטרך לבצע סדרתיות עבור חלק מהמאפיינים.
   - פעולה: כתיבת פונקציה save_analysis_record ב-AnalysisRecordRepository.

#### 4. הטמעת לוגיקת השוואת פרופילים והמלצות

4.1. פונקציה להשוואת פרופילי קבצים:
   - פיתוח פונקציה ב-FileProfileService שתקבל שני אובייקטים FileProfile ותחזיר מדד דמיון ביניהם (למשל, על בסיס דמיון קוסינוס של וקטורי שמות עמודות וחפיפה בקבוצות שמות העמודות).
   - פעולה: כתיבת פונקציה compare_file_profiles ב-FileProfileService.

4.2. פונקציה לאחזור פרופילים דומים ממסד הנתונים:
   - פיתוח פונקציה ב-FileProfileService שתקבל אובייקט FileProfile של קובץ חדש, תשלף את כל הפרופילים הקיימים מטבלת file_profiles ותשתמש בפונקציה compare_file_profiles כדי למצוא פרופילים דומים.
   - פעולה: כתיבת פונקציה get_similar_file_profiles ב-FileProfileService.

4.3. פונקציה לאחזור ניתוחים רלוונטיים עבור קובץ דומה:
   - פיתוח פונקציה ב-AnalysisService שתקבל נתיב של קובץ דומה ותשלוף את רשומות הניתוח שבוצעו עליו מטבלת analyses.
   - פעולה: כתיבת פונקציה get_analyses_for_file ב-AnalysisService.

4.4. פונקציה ליצירת המלצות ניתוח:
   - פיתוח פונקציה ב-AnalysisService שתקבל אובייקט FileProfile של הקובץ הנוכחי ואת רשימת הניתוחים שבוצעו על קבצים דומים.
   - הפונקציה תנתח את הניתוחים הקודמים ותציע ניתוחים רלוונטיים לקובץ הנוכחי על בסיס שמות העמודות הקיימים.
   - פעולה: כתיבת פונקציה generate_analysis_recommendations ב-AnalysisService.

#### 5. שילוב עם ממשק המשתמש (GUI)

5.1. הצגת המלצות ב-GUI:
   - עדכון ה-GUI כך שיקבל רשימה של המלצות ניתוח מ-AnalysisService.
   - הוספת אלמנטים UI להצגת ההמלצות (למשל, רשימה).
   - פעולה: שינוי קוד ב-gui.py להצגת המלצות.

5.2. אפשרות להרצת ניתוח מומלץ:
   - הוספת פונקציונליות ב-GUI המאפשרת למשתמש לבחור המלצה ולהריץ אותה.
   - העברת המידע הרלוונטי (סוג ניתוח, עמודות) ל-DataProcessing.
   - פעולה: הוספת אינטראקטיביות להמלצות ב-gui.py.

5.3. הצגת היסטוריית ניתוחים (אופציונלי):
   - שקילה להוסיף אפשרות למשתמש לראות את היסטוריית הניתוחים שבוצעו על קבצים דומים.
   - פעולה: (אם רלוונטי) הוספת אלמנטים UI להצגת היסטוריה ופונקציונליות לשליפת מידע זה מ-AnalysisService.

#### 6. בדיקות ושיפורים

6.1. בדיקות יחידה (Unit Tests):
   - כתיבת בדיקות יחידה עבור כל אחת מהפונקציות החדשות שפותחו (יצירת פרופיל, השוואה, שמירה, שליפה, יצירת המלצות).
   - פעולה: כתיבת קוד בדיקה.

6.2. בדיקות אינטגרציה (Integration Tests):
   - בדיקה שהמודולים השונים עובדים יחד כראוי (למשל, שטעינת קובץ, יצירת פרופיל ושמירתו במסד הנתונים מתבצעים בצורה נכונה).
   - פעולה: כתיבת קוד בדיקה.

6.3. בדיקות משתמש (User Testing):
   - בדיקה עם משתמשים כדי לקבל פידבק על השימושיות והרלוונטיות של ההמלצות.
   - פעולה: ביצוע סבב בדיקות עם משתמשים.

6.4. שיפורים ואיטרציה:
   - בהתבסס על תוצאות הבדיקות והפידבק, ביצוע שיפורים בקוד, באלגוריתמים ובעיצוב הממשק.
   - פעולה: חזרה על שלבים קודמים לפי הצורך.

### מבנה הפרויקט

כדי לארגן את הקוד בצורה טובה, אנחנו הולכים לחלק אותו לתיקיות לפי השכבות הארכיטקטוניות:

```
├── main.py
├── README.md
├── WorkPlan.md
├── domain/
│   ├── data_model.py
│   ├── data_loader.py
│   ├── data_filter.py
│   ├── intent_parser.py
│   └── data_processing.py
├── infrastructure/
│   ├── logger.py
│   ├── performance_monitor.py
│   └── export.py
├── service/
│   ├── file_profile_service.py
│   └── analysis_service.py
├── data_access/
│   ├── file_profile_repository.py
│   ├── analysis_record_repository.py
│   └── database_handler.py
├── common/
│   └── your_models.py
├── presentation/
│   └── gui.py
└── logs/
```

### סטטוס התקדמות

#### מה עשינו:
- הגדרנו את הארכיטקטורה החדשה
- תכננו את מבנה התיקיות והקבצים
- קיימות המחלקות הבסיסיות FileProfile ו-AnalysisRecord (אך הן דורשות שיפור)

#### מה לא עשינו:
- עדיין לא התחלנו לפתח את הפונקציונליות החדשה (עבודה עם מסד הנתונים, שכבת שירות, לוגיקת השוואה והמלצות)
- עדיין לא התחלנו לכתוב בדיקות