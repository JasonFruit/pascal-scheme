(define (int-list bottom top)
  (if (= bottom top) (list bottom)
      (cons bottom (int-list (+ bottom 1) top))))

(define (fac n)
  (if (= n 0) 1
      (* n (fac (- n 1)))))

(display (null? (display (symbol? (gensym)))))
(display (list? (map fac (int-list 1 10))))
(display (not (string? (quote asdf))))
(display (string? "asdf"))
