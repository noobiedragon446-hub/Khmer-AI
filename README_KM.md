# My Private AI — Android APK starter project

គម្រោងនេះជាគំរូកម្មវិធី Android សម្រាប់ប្រើផ្ទាល់ខ្លួន៖
- បង្កើតរូបភាពពី prompt
- ជ្រើសរូបថតពី Gallery ហើយផ្ញើទៅ backend សម្រាប់កែរូប
- បង្ហាញលទ្ធផល និងរក្សាទុកទៅ Gallery
- មាន PIN lock មូលដ្ឋានក្នុងកម្មវិធី
- API key រក្សាទុកនៅ backend មិនដាក់ក្នុង APK

## អ្វីដែលត្រូវដឹងមុន
នេះជាគម្រោង source code មិនមែន APK ដែលបាន build រួចទេ។ ត្រូវ build ដោយ Android Studio។ ការបង្កើត/កែរូបត្រូវការអ៊ីនធឺណិត និង OpenAI API key ដែលអាចមានការគិតថ្លៃ។ ការកែរូបដោយយករូបយោងប្រើ endpoint edit របស់ Images API; សមត្ថភាព និងម៉ូដែលអាចអាស្រ័យលើសិទ្ធិគណនី API។

## 1. ចាប់ផ្តើម backend
ត្រូវមានកុំព្យូទ័រដែលអាចដំណើរការ Python និងអ៊ីនធឺណិត។

```bash
cd backend
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
```

បង្កើត `.env` នៅក្នុង `backend/` ដោយចម្លងពី `.env.example` ហើយបញ្ចូល API key របស់អ្នក។ កុំចែករំលែក `.env` ឬ API key។

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

**សុវត្ថិភាព:** កុំបើក port 8000 ទៅអ៊ីនធឺណិតសាធារណៈ។ សម្រាប់ការសាកល្បងនៅផ្ទះ សូមភ្ជាប់ទូរស័ព្ទ និងកុំព្យូទ័រទៅ Wi-Fi ដូចគ្នា។ កំណត់ `API_TOKEN` ក្នុង `.env` ហើយដាក់ token ដូចគ្នាក្នុង Android app។ សម្រាប់ប្រើពិត គួរប្រើ HTTPS និងកំណត់ firewall។

## 2. កំណត់ Android app
បើក folder `android/` ដោយ Android Studio។ Gradle sync ហើយសូមកែ `BASE_URL` ក្នុង `MainActivity.kt`៖
- Emulator Android: `http://10.0.2.2:8000/`
- ទូរស័ព្ទពិត: `http://IP_ADDRESS_OF_YOUR_COMPUTER:8000/` (ឧ. `http://192.168.1.20:8000/`)

កែ `API_TOKEN` ក្នុង `MainActivity.kt` ឱ្យដូចនឹង backend `.env`។ សម្រាប់ប្រើប្រាស់ពិត គួរជំនួស token ថេរនេះដោយ login/session ដែលមានសុវត្ថិភាពជាង។ កុំប្រើ token សម្ងាត់ដែលអនុញ្ញាតសិទ្ធិ OpenAI ដោយផ្ទាល់នៅក្នុង app។

## 3. Build APK
1. បើក `android/` ក្នុង Android Studio។
2. រង់ចាំ Gradle Sync។
3. ជ្រើស Build > Build APK(s)។
4. APK សាកល្បងស្ថិតនៅ `android/app/build/outputs/apk/debug/app-debug.apk`។

## Privacy
រូបថតដែលអ្នកជ្រើសនឹងត្រូវផ្ញើទៅ backend និង OpenAI សម្រាប់កែរូប។ រូបលទ្ធផលរក្សាទុកក្នុង Gallery នៅពេលចុច Save។ មិនមាន Play Store ឬការចែករំលែកសាធារណៈនៅក្នុងគម្រោងនេះទេ។
