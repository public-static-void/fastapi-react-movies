import Loading from './Loading';
import MovieSection from './MovieSection';
import { MainPageFormValuesType } from '../types/form';
import { setMovieId } from '../state/SelectBoxSlice';
import { skipToken } from '@reduxjs/toolkit/query';
import { useAppDispatch, useAppSelector } from '../state/hooks';
import { useEffect } from 'react';
import { useFormikContext } from 'formik';
import { useMovieQuery, useMoviesQuery } from '../state/MovieManagerApi';

const MovieList = () => {
  const { setFieldValue, setStatus } =
    useFormikContext<MainPageFormValuesType>();
  const movieId = useAppSelector((state) => state.selectBox.movieId);
  const dispatch = useAppDispatch();
  const { data: movies, isLoading } = useMoviesQuery();
  const { data: movie } = useMovieQuery(movieId ?? skipToken);

  useEffect(() => {
    if (movie) {
      void setFieldValue('movieName', movie.name ?? '');
      void setFieldValue(
        'movieSeriesId',
        movie.series ? movie.series.id.toString() : ''
      );
      void setFieldValue(
        'movieSeriesNumber',
        movie.series_number ? movie.series_number.toString() : ''
      );
      void setFieldValue(
        'movieStudioId',
        movie.studio ? movie.studio.id.toString() : ''
      );
      void setFieldValue(
        'movieCategories',
        movie.categories.map((category) => category.id.toString())
      );
    }
  }, [movie, setStatus, setFieldValue]);

  return (
    <MovieSection title="Movie List">
      {isLoading ? (
        <div className="h-64">
          <Loading />
        </div>
      ) : (
        <select
          className="h-64 w-full bg-gray-100 dark:bg-gray-900"
          size={10}
          defaultValue={movieId ?? ''}
          onChange={(e) => {
            dispatch(setMovieId(e.target.value));
            setStatus('');
          }}
          data-testid="movies-listbox"
        >
          {movies?.map((movie) => (
            <option
              key={movie.id}
              value={movie.id}
              className="text-gray-900 bg-gray-100 hover:bg-gray-300 checked:text-gray-800 checked:bg-gray-200 dark:text-gray-100 dark:bg-gray-900 dark:hover:bg-gray-700 dark:checked:text-gray-200 dark:checked:bg-gray-800"
            >
              {movie.filename}
            </option>
          ))}
        </select>
      )}
    </MovieSection>
  );
};

export default MovieList;
