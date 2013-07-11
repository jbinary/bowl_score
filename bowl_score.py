#!/usr/bin/env python
import sys

INVALID_FORMAT = 'Invalid input data format'
LAST_FRAME = 10

class InvalidInputException(Exception):
    pass


def count_score(scores):
    """Given a list of knocked down pins on each turn return total score
       for a round.

       >>> count_score([10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10])
       300
       >>> count_score([9, 0, 3, 5, 6, 1, 3, 6, 8, 1, 5, 3, 2, 5, 8, 0, 7, 1, 8, 1])
       82
       >>> count_score([9, 0, 3, 7, 6, 1, 3, 7, 8, 1, 5, 5, 0, 10, 8, 0, 7, 3, 8, 10, 8])
       131
       >>> count_score([10, 3, 7, 6, 1, 10, 10, 10, 2, 8, 9, 0, 7, 3, 10, 10, 10])
       193
       >>> count_score([10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10])
       Traceback (most recent call last):
           ...
       InvalidInputException: Not enough balls
       >>> count_score([10, 10, 10, 10, 10, 10, 10, 10, 10, 2, 8])
       Traceback (most recent call last):
           ...
       InvalidInputException: Not enough balls
       >>> count_score([9, 7, 10, 10, 10, 10, 10, 10, 10, 10, 8, 1])
       Traceback (most recent call last):
           ...
       InvalidInputException: Frame 1 has invalid scores (9, 7)
       >>> count_score([-9, 0, 10, 10, 10, 10, 10, 10, 10, 10, 8, 1])
       Traceback (most recent call last):
           ...
       InvalidInputException: Frame 1 has invalid scores (-9, 0)
    """
    scores = scores[:]

    def get_ball():
        if not scores:
            raise InvalidInputException('No data for frame %s' % (frame,))
        return scores.pop(0)

    score = 0
    for frame in xrange(1, LAST_FRAME + 1):
        first_ball = get_ball()
        result = (first_ball, get_ball() if first_ball != 10 else 0)
        is_last_frame = frame == LAST_FRAME
        if not all(map(lambda score: 0 <= score <= 10, result)) or \
            (sum(result) > 10 and not is_last_frame):
            raise InvalidInputException('Frame %s has invalid scores %s' % (
                frame, result))

        frame_result = sum(result)
        if frame_result == 10:
            is_strike = result[0] == 10
            extra_balls = 2 if is_strike else 1
            frame_result += sum(scores[:extra_balls])
            if is_last_frame and len(scores) < extra_balls:
                raise InvalidInputException('Not enough balls')
        score += frame_result

    return score

if __name__ == '__main__':
    try:
        scores = map(int, sys.argv[1:])
    except ValueError:
        print INVALID_FORMAT
        sys.exit(1)

    try:
        print 'Result is: %s' % (count_score(scores),)
    except InvalidInputException as e:
        print INVALID_FORMAT, e.message
        sys.exit(2)
