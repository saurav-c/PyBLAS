#include <boost/python.hpp>
#include <boost/numeric/ublas/vector.hpp>
#include <boost/numeric/ublas/vector_expression.hpp>
#include <boost/numeric/ublas/matrix.hpp>
#include <boost/numeric/ublas/io.hpp>

#include <boost/python/module.hpp>
#include <boost/python/class.hpp>
#include <boost/python/operators.hpp>
#include <boost/operators.hpp>

#include <boost/python/def.hpp>
#include <boost/python/class.hpp>
#include <boost/python/tuple.hpp>
#include <boost/python/extract.hpp>

#include <boost/serialization/access.hpp>
#include <boost/serialization/string.hpp>
#include <boost/serialization/shared_ptr.hpp>
#include <boost/archive/text_oarchive.hpp>
#include <boost/smart_ptr/make_shared.hpp>

#include <sstream>
#include <boost/archive/text_iarchive.hpp>

using namespace boost::python;

typedef boost::numeric::ublas::vector<double> BaseVector;
typedef BaseVector::iterator Iter;
typedef BaseVector::reverse_iterator RevIter;

typedef boost::numeric::ublas::matrix<double> BaseMatrix;




class Vector: public BaseVector {
public: 
	Vector() : BaseVector() {}
	Vector(unsigned int size) : BaseVector(size) {}
	Vector(const Vector& v) : BaseVector(v) {}
	Vector(const BaseVector& v) : BaseVector(v) {}

	void insert(unsigned int index, double value) {(*this).insert_element(index, value);}

	void set_item(unsigned int index, double value) {(*this)(index) = value;}
	double get_item(unsigned int index) {return (*this)(index);}
	
	Iter begin_it() {return (*this).begin();}
	Iter end_it() {return (*this).end();}
	RevIter rbegin_it() {return (*this).rbegin();}
	RevIter rend_it() {return (*this).rend();}

    void print() {std::cout << (*this);}

	// TODO: Change these for natural command operators: + - * /
	void mul(double scalar) {
		*(this) *= scalar;
	}
	void div(double scalar) {
		*(this) /= scalar;
	}
	void add(Vector vec) {
		*(this) += vec;
	}
	void sub(Vector vec) {
		*(this) -= vec;
	}

    template<class Archive>
    void serialize(Archive &ar, const unsigned int version)
    {
        ar & boost::serialization::base_object<BaseVector>(*this);
    }
};


struct world_pickle_suite : boost::python::pickle_suite
{
    static
    boost::python::tuple
    getinitargs(const Vector& v)
    {
        return boost::python::make_tuple(v.size());
    }


    static
    boost::python::tuple
    getstate(const Vector& v)
    {
        std::ostringstream oss;
        {
            boost::archive::text_oarchive oa(oss);
            oa << v;
        }
        return boost::python::make_tuple(oss);
    }

    static
    void
    setstate(Vector& v, boost::python::tuple state)
    {
        using namespace boost::python;
        if (len(state) != 1) 
        {
            PyErr_SetObject(PyExc_ValueError,
                          ("expected 1-item tuple in call to __setstate__; got %s"
                           % state).ptr()
              );
          throw_error_already_set();
        }

        Vector new_vec;

        std::ostringstream oss = extract<std::ostringstream>(state[0])
        std::istringstream iss(oss.str())
        {
            boost::archive::text_iarchive ia(iss);
            ia >> new_vec;
        }

        v = new_vec;

        double first = extract<double>(state[0]);
        v.set_item(0, first);
    }
};


class Matrix: public BaseMatrix {
public:
	Matrix() : BaseMatrix() {}
	Matrix(unsigned int s1, unsigned int s2) : BaseMatrix(s1, s2) {}
	Matrix(const Matrix& mat) : BaseMatrix(mat) {}
    Matrix(const BaseMatrix& mat) : BaseMatrix(mat) {}

    void print() {std::cout << (*this);}

    double get(unsigned int row, unsigned int col) {return (*this)(row, col);}
    void set(unsigned int row, unsigned int col, double val) {(*this)(row, col) = val;}

};


double ip(const Vector& a, const Vector& b) {
    return inner_prod(a, b);
}

Matrix op(const Vector& a, const Vector& b) {
    BaseMatrix mat = outer_prod(a, b);
    return Matrix(mat);
}

Vector prod1(const Matrix& m, const Vector& v) {
    BaseVector vec = prod(m, v);
    return Vector(vec);
}

Matrix prod2(const Matrix& m, const Matrix& n) {
    BaseMatrix mat = prod(m, n);
    return Matrix(mat);
}




BOOST_PYTHON_MODULE(pyblas)
{
    class_<Vector, Vector*>("Vector")
    	.def(init<unsigned int>())
    	.def(init<Vector>())
    	.def("size", &Vector::size)
    	.def("resize", &Vector::resize)
    	.def("max_size", &Vector::max_size)
    	.def("empty", &Vector::empty)
    	.def("swap", &Vector::swap)
    	.def("insert_element", &Vector::insert)
    	.def("erase_element", &Vector::erase_element)
    	.def("clear", &Vector::clear)
    	.def("__getitem__", &Vector::get_item)
    	.def("__setitem__", &Vector::set_item)
    	.def("begin", &Vector::begin_it)
    	.def("end", &Vector::end_it)
    	.def("rbegin", &Vector::rbegin_it)
    	.def("rend", &Vector::rend_it)
    	.def("mul", &Vector::mul)
    	.def("div", &Vector::div)
    	.def("add", &Vector::add)
    	.def("sub", &Vector::sub)
        .def("show", &Vector::print)
        .def_pickle(world_pickle_suite())
    ;

    def("inner_prod", ip);
    def("outer_prod", op);
    def("prod1", prod1);
    def("prod2", prod2);

    class_<Iter>("Iterator");


    class_<Matrix, Matrix*>("Matrix")
    	.def(init<unsigned int, unsigned int>())
    	.def(init<Matrix>())
        .def("get", &Matrix::get)
        .def("set", &Matrix::set)
    	.def("resize", &Matrix::resize)
    	.def("rows", &Matrix::size1)
    	.def("cols", &Matrix::size2)
    	.def("clear", &Matrix::clear)
        .def("show", &Matrix::print)
    ;
}

