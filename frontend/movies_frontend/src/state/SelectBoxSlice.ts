import type { PayloadAction } from '@reduxjs/toolkit';
import { createSlice } from '@reduxjs/toolkit';
import type { SelectBoxSliceType } from '../types/state';

const initialState: SelectBoxSliceType = {
  availableId: null,
  selectedId: null,
  movieId: null,
};

const slice = createSlice({
  name: 'selectBox',
  initialState,
  reducers: {
    reset: () => initialState,
    setAvailableId: (state, action: PayloadAction<string>) => {
      state.availableId = action.payload;
    },
    setSelectedId: (state, action: PayloadAction<string>) => {
      state.selectedId = action.payload;
    },
    setMovieId: (state, action: PayloadAction<string>) => {
      state.movieId = action.payload;
    },
  },
});

export const { reset, setAvailableId, setSelectedId, setMovieId } =
  slice.actions;
export default slice.reducer;
