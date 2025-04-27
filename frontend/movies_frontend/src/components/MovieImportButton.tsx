import { useState } from 'react';
import type { HTTPExceptionType, MovieFileType } from '../types/api';
import { useMoviesImportMutation } from '../state/MovieManagerApi';
import type { FetchBaseQueryError } from '@reduxjs/toolkit/query';

const MovieImportButton = () => {
  const [importStatus, setImportStatus] = useState('');
  const [trigger] = useMoviesImportMutation();

  const onImportMovies = async () => {
    try {
      const data: MovieFileType[] = await trigger().unwrap();
      let count: number;
      if (Array.isArray(data)) {
        count = data.length;
      } else {
        count = 0;
      }
      if (count === 0) {
        setImportStatus('No movie files found');
      } else {
        setImportStatus(`Imported ${count} file${count > 1 ? 's' : ''}`);
      }
    } catch (error) {
      const { status, data } = error as FetchBaseQueryError;
      if (status !== 422) {
        const {
          detail: { message },
        } = data as HTTPExceptionType;
        setImportStatus(message ? message : 'Unknown Error');
      }
    }
  };
  return (
    <div className="p-4 my-4 mx-auto w-max border border-solid rounded-xl border-gray-400 dark:border-gray-600">
      <div className="flex justify-center">
        <button
          className="inline-block px-8 py-2 text-center text-lg font-semibold rounded-xl text-gray-100 bg-slate-700 hover:bg-slate-600 dark:text-gray-900 dark:bg-slate-300 dark:hover:bg-slate-400"
          type="button"
          onClick={() => {
            void onImportMovies();
          }}
        >
          Import Movies
        </button>
      </div>
      {importStatus ? (
        <div className="pt-3 text-center">{importStatus}</div>
      ) : (
        <div className="pt-3 text-center">Click to import movies</div>
      )}
    </div>
  );
};

export default MovieImportButton;
