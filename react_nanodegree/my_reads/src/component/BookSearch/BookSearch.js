import React from 'react';
import { Link } from 'react-router-dom';

import './book-search.css';
import * as booksAPI from '../../api/books-api';
import BookList from '../BookList';

class BookSearch extends React.Component {
  state = { query: '', books: [] };

  handleChange = (event) => {
    const query = event.target.value;

    this.setState({ query });
    this.searchBooks(query);
  };

  handleSubmit = (event) => {
    this.searchBooks(this.state.query);
    event.preventDefault();
  };

  searchBooks = (query) => {
    if (query) {
      booksAPI.search(query).then((booksData) => {
        console.log(booksData);
        this.setState({ books: booksData });
      });
    }
  };

  render() {
    return (
      <div>
        <Link className="close-search" to="/">Close</Link>
        <form onSubmit={this.handleSubmit}>
          <div className="search-books-input-wrapper">
            <input
              type="text"
              value={this.state.query}
              onChange={this.handleChange}
              placeholder="Search by title or author"
            />
          </div>
        </form>
        <BookList
          books={this.state.books}
          onShelfChanged={this.props.onShelfChanged}
        />
      </div>
    );
  }
}

export default BookSearch;
