#include <boost/python.hpp>
using namespace boost::python;


#include <boost/numeric/ublas/vector.hpp>


BOOST_PYTHON_MODULE(vector)
{
	class_<boost::numeric::ublas::vector<double>>("vector")
}

