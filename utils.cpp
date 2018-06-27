#include <boost/python.hpp>
#include <boost/numeric/ublas/vector.hpp>

#include <boost/python/module.hpp>
#include <boost/python/class.hpp>
#include <boost/python/operators.hpp>
#include <boost/operators.hpp>

using namespace boost::python;

typedef boost::numeric::ublas::vector<double> BaseVector;
typedef BaseVector::iterator Iter;
typedef BaseVector::reverse_iterator RevIter;


class Vector: public BaseVector {
public: 
	Vector() : BaseVector() {}
	Vector(unsigned int size) : BaseVector(size) {}
	Vector(const Vector& v) : BaseVector(v) {}

	void insert(unsigned int index, double value) {(*this).insert_element(index, value);}

	void set_item(unsigned int index, double value) {(*this)(index) = value;}
	double get_item(unsigned int index) {return (*this)(index);}
	
	Iter begin_it() {return (*this).begin();}
	Iter end_it() {return (*this).end();}
	RevIter rbegin_it() {return (*this).rbegin();}
	RevIter rend_it() {return (*this).rend();}

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
};



BOOST_PYTHON_MODULE(utils)
{
    class_<Vector>("Vector")
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
    	.def("inner_prod", inner_prod)
    ;

    class_<Iter>("Iterator");
}

