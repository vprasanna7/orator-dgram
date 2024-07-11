/// <reference types="vite/client" />

interface ImportMetaEnv {
    readonly VITE_DAILY_ROOM_URL: string
    readonly VITE_DAILY_API_KEY: string
  }
  
  interface ImportMeta {
    readonly env: ImportMetaEnv
  }
  
  declare module '@daily-co/daily-js' {
    export default DailyIframe;
  }