#!/usr/bin/env python3

# https://docs.python.org/3.4/reference/simple_stmts.html#grammar-token-assert_stmt

# -------
# imports
# -------

from io       import StringIO
from unittest import main, TestCase

from collections import OrderedDict 
from Netflix import netflix_read, netflix_eval, netflix_print, netflix_solve, get_movie_rating, get_customer_rating, predict, get_solutions, calculate_RMSE

# -----------
# TestNetflix
# -----------

class TestNetflix (TestCase) :
    # ----
    # read
    # ----

    def test_read_1 (self) :
        s    = "2043:\n1417435\n"
        to_predict = netflix_read(s)
        self.assertEqual(1, len(to_predict))
        self.assertEqual(1417435, (to_predict[2043])[0])

    def test_read_2 (self) :
        s    = "2043:\n1417435\n2312054\n462685\n"
        to_predict = netflix_read(s)
        self.assertEqual(1, len(to_predict))
        self.assertEqual(1417435, (to_predict[2043])[0])
        self.assertEqual(2312054, (to_predict[2043])[1])
        self.assertEqual(462685, (to_predict[2043])[2])

    def test_read_2 (self) :
        s    = "2043:\n1417435\n2312054\n462685\n10851:\n1417435\n1234567\n"
        to_predict = netflix_read(s)
        self.assertEqual(2, len(to_predict))
        self.assertEqual(1417435, (to_predict[2043])[0])
        self.assertEqual(2312054, (to_predict[2043])[1])
        self.assertEqual(462685, (to_predict[2043])[2])
        self.assertEqual(1417435, (to_predict[10851])[0])
        self.assertEqual(1234567, (to_predict[10851])[1])

    # ----  
    # get_movie_rating
    # ----

    def test_get_movie_rating_1(self):
        rating = get_movie_rating(4335)
        self.assertEqual(3.779, rating)

    # ----     
    # get_customer_rating
    # ----

    def test_get_customer_rating_1(self):
        rating = get_customer_rating(1585790)
        self.assertEqual(3.41666667, round(rating, 8))


    # ----     
    # get_solutions
    # ----

    def test_get_solutions_1(self):
        solutions_dict = get_solutions()
        movie_ratings = solutions_dict[1]
        self.assertEqual(4, movie_ratings[0])


    # ----
    # predict
    # ----

    def test_predict_1(self):
        rating = predict(4335, 1585790)
        self.assertEqual(3.6, rating)


    # ------------
    # calcualate_RMSE
    # ------------    

    def test_calculate_RMSE(self):
        to_predict_dict = OrderedDict([(1585790, [2, 3, 4])])
        solutions_dict = OrderedDict([(1585790, [4, 1, 7])])
        rmse = calculate_RMSE(to_predict_dict, solutions_dict)
        self.assertEqual( 2.38047614285, round(rmse, 11))

    def test_calculate_RMSE(self):
        to_predict_dict = OrderedDict([(1585790, [2, 3]), (2484454, [4])])
        solutions_dict = OrderedDict([(1585790, [4, 1]), (2484454, [7])])
        rmse = calculate_RMSE(to_predict_dict, solutions_dict)
        self.assertEqual( 2.38047614285, round(rmse, 11))

    # ----
    # eval
    # ----

    def test_eval_1 (self) :
        to_predict_dict = OrderedDict([(4335, [1585790, 2484454, 756299])])
        predictions_dict = netflix_eval(to_predict_dict)
        self.assertEqual(1, len(predictions_dict))
        movie_ratings = predictions_dict[4335]
        self.assertEqual(3, len(movie_ratings))
        self.assertTrue(movie_ratings[0] >= 1)
        self.assertTrue(movie_ratings[0] <= 5)
        self.assertTrue(movie_ratings[1] >= 1)
        self.assertTrue(movie_ratings[1] <= 5)
        self.assertTrue(movie_ratings[2] >= 1)
        self.assertTrue(movie_ratings[2] <= 5)

    def test_eval_2 (self) :
        to_predict_dict = OrderedDict([(4335, [1585790, 2484454, 756299]), (1234, [1585790, 1654988])])
        predictions_dict = netflix_eval(to_predict_dict)
        self.assertEqual(2, len(predictions_dict))
        movie_ratings = predictions_dict[4335]
        self.assertEqual(3, len(movie_ratings))
        self.assertTrue(movie_ratings[0] >= 1)
        self.assertTrue(movie_ratings[0] <= 5)
        self.assertTrue(movie_ratings[1] >= 1)
        self.assertTrue(movie_ratings[1] <= 5)
        self.assertTrue(movie_ratings[2] >= 1)
        self.assertTrue(movie_ratings[2] <= 5)
        movie_ratings = predictions_dict[1234]
        self.assertEqual(2, len(movie_ratings))
        self.assertTrue(movie_ratings[0] >= 1)
        self.assertTrue(movie_ratings[0] <= 5)
        self.assertTrue(movie_ratings[1] >= 1)
        self.assertTrue(movie_ratings[1] <= 5)

    # -----
    # print
    # -----

    def test_print_1 (self) :
        w = StringIO()
        predictions_dict = OrderedDict([(2043, [3.4, 4.1, 1.9])])
        netflix_print(w, predictions_dict)
        self.assertEqual(w.getvalue(), "2043:\n3.4\n4.1\n1.9\n")

    def test_print_2 (self) :
        w = StringIO()
        predictions_dict = OrderedDict([(2043, [3.4, 4.1, 1.9]), (10851, [4.3, 1.4, 2.8])])
        netflix_print(w, predictions_dict)
        self.assertEqual(w.getvalue(), "2043:\n3.4\n4.1\n1.9\n10851:\n4.3\n1.4\n2.8\n")

    # -----
    # solve
    # -----
    def test_solve (self) :
        r = StringIO("1:\n30878\n2647871\n1283744")
        w = StringIO()
        netflix_solve(r, w)
        self.assertEqual(w.getvalue(), "1:\n3.7\n3.5\n3.6\nRMSE: 0.48")
        #4 4 3
        #-.3 .5 .6
        #.09 .25 .36
        #0.2333...
        #0.48304589
# ----
# main
# ----

if __name__ == "__main__" :
    main()

"""
% coverage3 run --branch TestNetflix.py >  TestNetflix.out 2>&1



% coverage3 report -m                   >> TestNetflix.out



% cat TestNetflix.out
.......
----------------------------------------------------------------------
Ran 7 tests in 0.001s

OK
Name          Stmts   Miss Branch BrMiss  Cover   Missing
---------------------------------------------------------
Netflix          18      0      6      0   100%
TestNetflix      33      1      2      1    94%   79
---------------------------------------------------------
TOTAL            51      1      8      1    97%
"""
