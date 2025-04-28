# Software Development Work Plan 📊

## English Section

### Architecture Overview
1. **Updated Architecture with SQLite Integration**:

   **DataModel (Significantly Expanded)**:
   - Will continue handling data loading, filtering, and sorting.
   - **Analysis History Database Management**: SQLite implementation. We need to define an appropriate schema (tables) for storing analysis history:
     - Table `analyses`: analysis_id (INTEGER PRIMARY KEY), file_path (TEXT), query (TEXT), analysis_type (TEXT), column_names (TEXT), settings (TEXT), results_path (TEXT), timestamp (DATETIME).
     - Additional tables may be needed for many-to-many relationships to store analysis settings in a more structured way.
   - **File Profiles Management**: SQLite implementation with table structure:
     - Table `file_profiles`: file_path (TEXT PRIMARY KEY), column_names (TEXT), column_types (TEXT), basic_stats (TEXT), column_vectors (TEXT).
     - column_vectors can contain vector representation of column names. We'll need to determine an appropriate format for storing vectors in text fields (e.g., comma-separated list).
   - Will handle recommendation logic, using data stored in SQLite.

   **IntentParser**: Will continue as before but can retrieve information from file profiles in SQLite to improve column identification.

   **DataProcessing**: No significant changes.

   **GUI**: Will be updated to display information from SQLite database (recommendations, analysis history).

2. **Operation Details with SQLite Integration**:

   **File Type Identification**:
   - When a file is loaded, DataModel creates a profile.
   - This profile is stored in the file_profiles table in SQLite.
   - Comparison methods (cosine similarity, group comparison) will operate on data retrieved from the file_profiles table.

   **Analysis History Storage**:
   - At the end of each analysis, a new record is inserted into the analyses table in SQLite with all relevant details.

   **Analysis Recommendations**:
   - When a new file is loaded, DataModel retrieves its profile from the file_profiles table.
   - It compares this profile to other profiles in the table.
   - Based on similar files, it retrieves analysis records from the analyses table to see what analyses were performed in the past.
   - Recommendations are formulated based on criteria (file similarities, analysis frequency, relevance to current columns).

   **User Interface (GUI)**:
   - GUI will use SQL queries to retrieve relevant recommendations from the analyses table and display them to the user.
   - Actions like selecting a previous analysis or displaying previous results will be based on retrieving data from SQLite.

3. **Code Structure Changes with SQLite Interaction**:

   **data_model.py**:
   - Will need to include functions for connecting to SQLite database, executing queries (INSERT, SELECT, UPDATE).
   - Functions like create_file_profile, compare_file_profiles, add_analysis_record, get_relevant_analyses, generate_analysis_recommendations will now include SQL code to store and retrieve information from SQLite.

   **gui.py**:
   - Will need to communicate with DataModel to get the list of recommendations. DataModel will handle retrieving information from SQLite.
   - When a user selects a recommended analysis, GUI sends the details to DataModel, which can retrieve the original settings from SQLite if needed.

   **intent_parser.py**: Can gain access (through DataModel) to the file_profiles table to compare column names with those mentioned by the user in queries.

   **data_processing.py**: Should not be directly affected by SQLite usage.

4. **Implementation Example**:

   - User loads "sales_data_2023.csv".
   - DataModel creates a profile and saves it in the file_profiles table.
   - User runs "graph of revenue by date".
   - DataModel saves a record in the analyses table.
   - User loads "sales_data_2024.csv".
   - DataModel creates a profile and saves it in the file_profiles table.
   - DataModel queries file_profiles to find similar files.
   - Assuming "sales_data_2023.csv" is found similar, DataModel queries the analyses table to find analyses performed on this file.
   - DataModel identifies the analysis "graph of revenue by date" and creates a tailored recommendation for the new file ("Would you like to create a graph of total sales by order date...?").
   - GUI retrieves the recommendation from DataModel and displays it.

5. **Challenges and Considerations**:

   - **Database Schema Design**: Important to plan tables and fields carefully to enable efficient information retrieval.
   - **Query Performance**: As the database grows, we'll need to ensure the queries we perform are efficient. We may need to add indexes on certain columns in tables.
   - **Code Complexity**: Integration with a database will add complexity to DataModel code. We'll need to manage connections, execute queries, and handle errors.
   - **Serialization**: Pay attention to how complex data structures (like vectors or statistics) are stored in text fields in SQLite. Serialization (e.g., to JSON) will be needed when inserting data and restoring it when retrieving.

### Code File Review:
- **data_model.py**: Handles data loading, filtering, sorting, and initial query history management.
- **data_processing.py**: Contains data processing functions (graphs, averages, counts, dates).
- **export.py**: Responsible for exporting data in various formats (Excel, JSON, HTML, CSV).
- **gui.py**: Graphical user interface (GUI) code using Tkinter.
- **intent_parser.py**: Analyzes user queries to identify intent and relevant columns.
- **logger.py**: Handles event logging.
- **main.py**: Main entry point of the application.
- **performance_monitor.py**: Monitors application performance.
- **README.md**: Basic documentation file.
- **WorkPlan.md**: Our work plan.

### Implementation Status:

#### Phase 1: Database Infrastructure Setup (SQLite)
1.1. **Database Schema Design**: Not implemented yet.
1.2. **DatabaseHandler Class Implementation**: Not implemented yet.
1.3. **Database Table Creation**: Not implemented yet.

#### Phase 2: FileProfile Module Development
2.1. **FileProfile Class Definition**: Partially implemented.
2.2. **File Profile Creation Function**: Partially implemented.
2.3. **Function to Save File Profile in Database**: Not implemented yet.

#### Phase 3: AnalysisRecord Module Development
3.1. **AnalysisRecord Class Definition**: Partially implemented.
3.2. **Function to Save Analysis Record in Database**: Not implemented yet.

#### Phase 4: Profile Comparison Logic and Recommendations
4.1. **Function for Comparing File Profiles**: Not implemented yet.
4.2. **Function to Retrieve Similar Profiles from Database**: Not implemented yet.
4.3. **Function to Retrieve Relevant Analyses for Similar Files**: Not implemented yet.
4.4. **Function to Generate Analysis Recommendations**: Not implemented yet.

#### Phase 5: User Interface Integration (GUI)
5.1. **Display Recommendations in GUI**: Not implemented yet.
5.2. **Option to Run Recommended Analysis**: Not implemented yet.
5.3. **Display Analysis History (Optional)**: Not implemented yet.

#### Phase 6: Testing and Improvements
6.1. **Unit Tests**: Likely not implemented yet.
6.2. **Integration Tests**: Likely not implemented yet.
6.3. **User Testing**: Not relevant at this stage.
6.4. **Improvements and Iteration**: Not relevant at this stage.

---

## החלק העברי

### ארכיטקטורה
1. **ארכיטקטורה מעודכנת עם דגש על SQLite**:

   **DataModel (מורחב מאוד)**:
   - ימשיך לטפל בטעינת נתונים, סינון ומיון.
   - **ניהול מאגר נתונים של ניתוחים (Analysis History Database)**: כאן SQLite נכנס לתמונה. נצטרך להגדיר סכמה (טבלאות) מתאימה לשמירת היסטוריית הניתוחים:
     - טבלת analyses: analysis_id (INTEGER PRIMARY KEY), file_path (TEXT), query (TEXT), analysis_type (TEXT), column_names (TEXT), settings (TEXT), results_path (TEXT), timestamp (DATETIME).
     - ייתכן שנצטרך טבלאות נוספות ליחסים רבים-לרבים אם נרצה לשמור הגדרות ניתוח בצורה יותר מובנית.
   - **ניהול פרופילי קבצים (File Profiles)**: גם כאן SQLite יכול לשמש:
     - טבלת file_profiles: file_path (TEXT PRIMARY KEY), column_names (TEXT), column_types (TEXT), basic_stats (TEXT), column_vectors (TEXT).
     - column_vectors יכול להכיל ייצוג וקטורי של שמות העמודות. נצטרך להחליט על פורמט מתאים לאחסון הווקטור בתוך שדה טקסט (למשל, רשימה מופרדת בפסיקים).
   - יטפל בלוגיקת ההמלצות, תוך שימוש בנתונים השמורים ב-SQLite.

   **IntentParser**: ימשיך כרגיל, אך יוכל לשלוף מידע מפרופילי הקבצים ב-SQLite כדי לשפר את זיהוי העמודות.

   **DataProcessing**: ללא שינויים מהותיים.

   **GUI**: יתעדכן כדי להציג מידע ממאגר הנתונים של SQLite (המלצות, היסטוריה של ניתוחים).

2. **פירוט הפעולות עם התייחסות ל-SQLite**:

   **זיהוי סוג קובץ**:
   - כשקובץ נטען, DataModel ייצור פרופיל.
   - הפרופיל הזה יישמר בטבלת file_profiles ב-SQLite.
   - שיטות ההשוואה (דמיון קוסינוס, השוואת קבוצות) יפעלו על הנתונים שנשלפו מטבלת file_profiles.

   **שמירת היסטוריית ניתוחים**:
   - בסיום כל ניתוח, רשומה חדשה תוכנס לטבלת analyses ב-SQLite, עם כל הפרטים הרלוונטיים.

   **המלצות ניתוח**:
   - כשקובץ חדש נטען, DataModel ישלוף את הפרופיל שלו מטבלת file_profiles.
   - הוא ישווה אותו לפרופילים אחרים בטבלה.
   - בהתבסס על קבצים דומים, הוא ישלוף את רשומות הניתוח מטבלת analyses כדי לראות אילו ניתוחים בוצעו בעבר.
   - ההמלצות יגובשו על סמך הקריטריונים שציינת (דמיון קבצים, תדירות ניתוחים, רלוונטיות לעמודות הנוכחיות).

   **ממשק משתמש (GUI)**:
   - ה-GUI ישתמש בשאילתות SQL כדי לשלוף את ההמלצות הרלוונטיות מטבלת analyses ולהציג אותן למשתמש.
   - פעולות כמו בחירת ניתוח קודם או הצגת תוצאות קודמות יתבססו על שליפת נתונים מ-SQLite.

3. **שינויים בקוד (מבנה) עם דגש על אינטראקציה עם SQLite**:

   **data_model.py**:
   - יצטרך לכלול פונקציות להתחברות למסד הנתונים SQLite, ביצוע שאילתות (INSERT, SELECT, UPDATE).
   - פונקציות כמו create_file_profile, compare_file_profiles, add_analysis_record, get_relevant_analyses, generate_analysis_recommendations יכללו כעת קוד SQL כדי לאחסן ולשלוף מידע מ-SQLite.

   **gui.py**:
   - יצטרך לתקשר עם DataModel כדי לקבל את רשימת ההמלצות. DataModel כבר יטפל בשליפת המידע מ-SQLite.
   - כאשר משתמש בוחר ניתוח מומלץ, ה-GUI ישלח את הפרטים ל-DataModel, שיכול לשלוף את ההגדרות המקוריות מ-SQLite אם צריך.

   **intent_parser.py**: יכול לקבל גישה (דרך DataModel) לטבלת file_profiles כדי להשוות שמות עמודות עם אלה שהמשתמש הזכיר בשאילתה.

   **data_processing.py**: לא אמור להיות מושפע ישירות משימוש ב-SQLite.

4. **דוגמה מפורטת עם שילוב SQLite**:

   - המשתמש טוען "sales_data_2023.csv".
   - DataModel יוצר פרופיל ושומר אותו בטבלת file_profiles.
   - המשתמש מריץ "גרף של הכנסות לפי תאריך".
   - DataModel שומר רשומה בטבלת analyses.
   - המשתמש טוען "sales_data_2024.csv".
   - DataModel יוצר פרופיל ושומר אותו בטבלת file_profiles.
   - DataModel מבצע שאילתות על file_profiles כדי למצוא קבצים דומים.
   - בהנחה שנמצא "sales_data_2023.csv" כדומה, DataModel מבצע שאילתות על טבלת analyses כדי למצוא ניתוחים שבוצעו על קובץ זה.
   - DataModel מזהה את הניתוח "גרף של הכנסות לפי תאריך" ויוצר המלצה מותאמת לקובץ החדש ("האם תרצה ליצור גרף של סך המכירות לפי תאריך ההזמנה...?").
   - ה-GUI שולף את ההמלצה מ-DataModel ומציג אותה.

5. **אתגרים ושיקולים עם דגש על SQLite**:

   - **עיצוב סכמת מסד הנתונים**: חשוב לתכנן היטב את הטבלאות והשדות כדי לאפשר אחזור יעיל של מידע.
   - **ביצועים של שאילתות**: ככל שהמסד יגדל, נצטרך לוודא שהשאילתות שאנחנו מבצעים יעילות. ייתכן שנצטרך להוסיף אינדקסים על עמודות מסוימות בטבלאות.
   - **מורכבות קוד**: השילוב עם מסד נתונים יוסיף מורכבות לקוד של DataModel. נצטרך לנהל חיבורים, לבצע שאילתות ולטפל בשגיאות.
   - **סדרתיות (Serialization)**: שימו לב איך אתם מאחסנים מבני נתונים מורכבים (כמו וקטורים או סטטיסטיקות) בתוך שדות טקסט ב-SQLite. תצטרכו לבצע סדרתיות (למשל, ל-JSON) כשאתם מכניסים נתונים ולשחזר אותם כשאתם שולפים.

### סקירה של קבצי הקוד:
- **data_model.py**: מטפל בטעינת נתונים, סינון, מיון, ויש בו התחלה של טיפול בהיסטוריית שאילתות.
- **data_processing.py**: מכיל פונקציות לעיבוד הנתונים (גרפים, ממוצעים, ספירות, תאריכים).
- **export.py**: אחראי על ייצוא הנתונים בפורמטים שונים (Excel, JSON, HTML, CSV).
- **gui.py**: קוד ממשק המשתמש הגרפי (GUI) באמצעות Tkinter.
- **intent_parser.py**: מנתח את שאילתות המשתמש כדי לזהות את הכוונה ואת העמודות הרלוונטיות.
- **logger.py**: מטפל ברישום אירועים (logging).
- **main.py**: נקודת הכניסה הראשית של האפליקציה.
- **performance_monitor.py**: מנטר את ביצועי האפליקציה.
- **README.md**: קובץ תיעוד בסיסי.
- **WorkPlan.md**: תוכנית העבודה שלנו.

### סטטוס התקדמות:

#### שלב 1: הקמת תשתית מסד הנתונים (SQLite)
1.1. **תכנון סכמת מסד הנתונים**: טרם בוצע.
1.2. **הטמעת מחלקת DatabaseHandler**: טרם בוצע.
1.3. **יצירת טבלאות במסד הנתונים**: טרם בוצע.

#### שלב 2: פיתוח מודול FileProfile
2.1. **הגדרת מחלקת FileProfile**: בוצע חלקית.
2.2. **פונקציה ליצירת פרופיל קובץ**: בוצע חלקית.
2.3. **פונקציה לשמירת פרופיל קובץ במסד הנתונים**: טרם בוצע.

#### שלב 3: פיתוח מודול AnalysisRecord
3.1. **הגדרת מחלקת AnalysisRecord**: בוצע חלקית.
3.2. **פונקציה לשמירת רשומת ניתוח במסד הנתונים**: טרם בוצע.

#### שלב 4: הטמעת לוגיקת השוואת פרופילים והמלצות
4.1. **פונקציה להשוואת פרופילי קבצים**: טרם בוצע.
4.2. **פונקציה לאחזור פרופילים דומים ממסד הנתונים**: טרם בוצע.
4.3. **פונקציה לאחזור ניתוחים רלוונטיים עבור קובץ דומה**: טרם בוצע.
4.4. **פונקציה ליצירת המלצות ניתוח**: טרם בוצע.

#### שלב 5: שילוב עם ממשק המשתמש (GUI)
5.1. **הצגת המלצות ב-GUI**: טרם בוצע.
5.2. **אפשרות להרצת ניתוח מומלץ**: טרם בוצע.
5.3. **הצגת היסטוריית ניתוחים (אופציונלי)**: טרם בוצע.

#### שלב 6: בדיקות ושיפורים
6.1. **בדיקות יחידה (Unit Tests)**: כנראה שטרם בוצע.
6.2. **בדיקות אינטגרציה (Integration Tests)**: כנראה שטרם בוצע.
6.3. **בדיקות משתמש (User Testing)**: טרם רלוונטי בשלב הזה.
6.4. **שיפורים ואיטרציה**: טרם רלוונטי בשלב הזה.

### סיכום מה בוצע ומה נותר

**מה בוצע**:
- יש מבנה בסיסי לאפליקציה (GUI, עיבוד נתונים, ניתוח כוונות).
- יש מחלקות FileProfile ו-AnalysisRecord (אבל צריך לשפר אותן).
- יש פונקציה לטעינת נתונים.

**מה נותר**:
- הכי חשוב: הטמעת SQLite (מחלקה, סכמה, פעולות מסד נתונים).
- שיפור FileProfile ו-AnalysisRecord.
- פונקציות להשוואת פרופילים ויצירת המלצות.
- עדכון ה-GUI להצגת המלצות.
- הוספת בדיקות.