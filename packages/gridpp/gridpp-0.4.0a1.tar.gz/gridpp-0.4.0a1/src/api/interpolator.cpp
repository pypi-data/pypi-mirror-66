#include "gridpp.h"

#if 0
float gridpp::Interpolator::interpolate(const gridpp::Points& points, const vec& values, float lat, float lon, float altitude, float land_area_fraction) const {
    gridpp::util::not_implemented_error();
    return gridpp::MV;
}
#endif
gridpp::Nearest::Nearest(int num) : m_num(num), gridpp::Interpolator::Interpolator() {

}
float gridpp::Nearest::interpolate(const gridpp::Points& points, const vec& values, float lat, float lon, float altitude, float land_area_fraction) const {
    ivec indices = points.get_closest_neighbours(lat, lon, m_num);
    float sum = 0;
    int count = 0;
    for(int i = 0; i < indices.size(); i++) {
        float value = values[indices[i]];
        if(gridpp::util::is_valid(value)) {
            sum += value;
            count++;
        }
    }
    if(count > 0)
        return sum / count;
    else
        return gridpp::MV;
}
gridpp::Interpolator* gridpp::Nearest::clone() const {
    gridpp::Interpolator* val = new gridpp::Nearest(m_num);
    return val;
}
