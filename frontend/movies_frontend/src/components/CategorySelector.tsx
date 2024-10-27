import Loading from './Loading';
import MovieSection from './MovieSection';
import {
  useCategoriesQuery,
  useMovieCategoryAddMutation,
  useMovieCategoryDeleteMutation,
  useMovieQuery,
} from '../state/MovieManagerApi';
import { FetchBaseQueryError, skipToken } from '@reduxjs/toolkit/query';
import { Field, useFormikContext } from 'formik';
import { HTTPExceptionType, MovieType } from '../types/api';
import { MainPageFormValuesType } from '../types/form';
import { useAppSelector } from '../state/hooks';

const CategorySelector = () => {
  const formik = useFormikContext<MainPageFormValuesType>();
  const movieId = useAppSelector((state) => state.selectBox.movieId);
  const [movieCategoryAddTrigger] = useMovieCategoryAddMutation();
  const [movieCategoryDeleteTrigger] = useMovieCategoryDeleteMutation();
  const { data: categories, isLoading } = useCategoriesQuery();
  const { data: movie } = useMovieQuery(movieId ? movieId : skipToken);

  const onUpdateCategory = async (categoryId: string, selected: boolean) => {
    if (movieId) {
      const trigger = selected
        ? movieCategoryAddTrigger
        : movieCategoryDeleteTrigger;
      const categoryName = categories?.find(
        (category) => category.id === +categoryId
      )?.name;
      try {
        const data: MovieType = await trigger({
          categoryId: categoryId,
          movieId: movieId,
        }).unwrap();
        formik.setStatus(
          `Successfully ${selected ? 'added' : 'removed'} category ${categoryName} ${
            selected ? 'to' : 'from'
          } ${data.name}`
        );
      } catch (error) {
        const { status, data } = error as FetchBaseQueryError;
        await formik.setFieldValue(
          'movieCategories',
          movie?.categories.map((category) => category.id.toString())
        );
        if (status !== 422) {
          const {
            detail: { message },
          } = data as HTTPExceptionType;
          formik.setStatus(message ? message : 'Unknown server error');
        }
      }
    }
  };

  return (
    <MovieSection title="Categories">
      <div className="h-72">
        {isLoading ? (
          <Loading />
        ) : (
          <fieldset disabled={!movieId}>
            <div className="grid grid-cols-3 gap-1 h-72 overflow-y-scroll">
              {categories?.map((category) => (
                <div key={category.id}>
                  <label>
                    <Field
                      type="checkbox"
                      name="movieCategories"
                      value={category.id.toString()}
                      onChange={(e: React.ChangeEvent<HTMLInputElement>) => {
                        formik.handleChange(e);
                        void onUpdateCategory(e.target.value, e.target.checked);
                      }}
                    />{' '}
                    {category.name}
                  </label>
                </div>
              ))}
            </div>
          </fieldset>
        )}
      </div>
    </MovieSection>
  );
};

export default CategorySelector;
