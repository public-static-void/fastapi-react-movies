import { configureStore } from '@reduxjs/toolkit';
import SelectBoxSlice from './SelectBoxSlice';
import MovieManagerApi from './MovieManagerApi';

export const createNewStore = () =>
  configureStore({
    reducer: {
      [MovieManagerApi.reducerPath]: MovieManagerApi.reducer,
      selectBox: SelectBoxSlice,
    },
    middleware: (getDefaultMiddleware) =>
      getDefaultMiddleware().concat(MovieManagerApi.middleware),
  });

export const store = createNewStore();

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
