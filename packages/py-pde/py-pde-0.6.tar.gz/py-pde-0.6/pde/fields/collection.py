'''
Defines a collection of fields to represent multiple fields defined on a common
grid.

.. codeauthor:: David Zwicker <david.zwicker@ds.mpg.de>
'''

import json
from typing import (Sequence, Optional, Union, Any, Dict,
                    List, Iterator)  # @UnusedImport

import numpy as np

from .base import FieldBase, DataFieldBase
from .scalar import ScalarField
from ..grids.base import GridBase



class FieldCollection(FieldBase):
    """ Collection of fields defined on the same grid """


    def __init__(self, fields: Sequence[DataFieldBase],
                 data=None,
                 copy_fields: bool = False,
                 label: Optional[str] = None):
        """ 
        Args:
            fields:
                Sequence of the individual fields
            data (:class:`numpy.ndarray`):
                Data of the fields. If `None`, the data is instead taken from
                the individual fields given by `fields`.
            copy_fields (bool):
                Flag determining whether the individual fields given in `fields`
                are copied. 
            label (str): Label of the field collection
            
        Warning:
            If `data` is given and `copy_fields == False`, the data in the
            individual fields is overwritten by the associated `data`.
        """
        if isinstance(fields, FieldCollection):
            # support assigning a field collection for convenience
            fields = fields.fields
            
        if len(fields) == 0:
            raise ValueError('At least one field must be defined')
        
        # check if grids are compatible
        grid = fields[0].grid
        if any(grid != f.grid for f in fields[1:]):
            grids = [f.grid for f in fields]
            raise RuntimeError(f'Grids are incompatible: {grids}')

        # create the list of underlying fields        
        if copy_fields:
            self._fields = [field.copy() for field in fields]
        else:
            self._fields = fields  # type: ignore
        
        # extract data from individual fields
        new_data: List[np.ndarray] = []
        self._slices: List[slice] = []
        dof = 0  # count local degrees of freedom
        for field in self.fields:
            if not isinstance(field, DataFieldBase):
                raise RuntimeError('Individual fields must be of type '
                                   'DataFieldBase. FieldCollections cannot be '
                                   'nested')
            start = len(new_data)
            this_data = field._data_flat
            new_data.extend(this_data)
            self._slices.append(slice(start, len(new_data)))
            dof += len(this_data)
                
        # combine into one data field
        data_shape = (dof,) + grid.shape
        if data is None:
            data = np.array(new_data, dtype=np.double)
        else:
            data = np.asarray(data, dtype=np.double)
            if data.shape != data_shape:
                data = np.array(np.broadcast_to(data, data_shape))
        assert data.shape == data_shape
        
        # initialize the class
        super().__init__(grid, data, label=label)        
            
        # link the data of the original fields back to self._data if they were
        # not copied
        if not copy_fields:
            for i, field in enumerate(self.fields):
                field_shape = field.data.shape
                field._data_flat = self.data[self._slices[i]]
                
                # check whether the field data is based on our data field
                assert field.data.base is self.data
                assert field.data.shape == field_shape
         
         
    def __repr__(self):
        """ return instance as string """
        fields = []
        for f in self.fields:
            name = f.__class__.__name__
            if f.label:
                fields.append(f'{name}(..., label="{f.label}")')
            else:
                fields.append(f'{name}(...)')
        return f"{self.__class__.__name__}({', '.join(fields)})"

        
    def __len__(self):
        """ return the number of stored fields """
        return len(self.fields)
    
    
    def __iter__(self) -> Iterator[DataFieldBase]:
        """ return iterator over the actual fields """
        return iter(self.fields)
    
    
    def __getitem__(self, index: Union[int, str]) -> DataFieldBase:
        """ return a specific field """
        if isinstance(index, int):
            # simple numerical index
            return self.fields[index]
        
        elif isinstance(index, str):
            # index specifying the label of the field
            for field in self.fields:
                if field.label == index:
                    return field
            raise KeyError(f'No field with name {index}')
        
        else:
            raise TypeError(f'Unsupported index {index}')

        
    def __setitem__(self, index: int, value):
        """ set the value of a specific field """
        # We need to load the field and set data explicitly
        # WARNING: Do not use `self.fields[index] = value`, since this would
        # break the connection between the data fields 
        if isinstance(index, int):
            # simple numerical index
            self.fields[index].data = value
            
        elif isinstance(index, str):
            # index specifying the label of the field
            for field in self.fields:
                if field.label == index:
                    field.data = value
                    break
            else:
                raise KeyError(f'No field with name {index}')

        else:
            raise TypeError(f'Unsupported index {index}')


    @property
    def fields(self) -> List[DataFieldBase]:
        """ list: the fields of this collection """
        return self._fields

        
    def __eq__(self, other):
        """ test fields for equality, ignoring the label """
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.fields == other.fields
    
        
    @classmethod
    def from_state(cls, attributes: Dict[str, Any],
                   data: np.ndarray = None) -> "FieldCollection":
        """ create a field collection from given state.
        
        Args:
            attributes (dict):
                The attributes that describe the current instance
            data (:class:`numpy.ndarray`, optional):
                Data values at support points of the grid defining all fields
        """
        if 'class' in attributes:
            class_name = attributes.pop('class')
            assert class_name == cls.__name__
        
        # restore the individual fields (without data)
        fields = [FieldBase.from_state(field_state)
                  for field_state in attributes.pop('fields')]
        
        return cls(fields, data=data, **attributes)  # type: ignore


    @classmethod
    def _from_hdf_dataset(cls, dataset) -> "FieldCollection":
        """ construct the class by reading data from an hdf5 dataset """
        # copy attributes from hdf
        attributes = dict(dataset.attrs)
        
        # determine class
        class_name = json.loads(attributes.pop('class'))
        assert class_name == cls.__name__
        
        # determine the fields
        field_attrs = json.loads(attributes.pop('fields'))
        fields = [DataFieldBase._from_hdf_dataset(dataset[f"field_{i}"])
                  for i in range(len(field_attrs))]
        
        # unserialize remaining attributes
        attributes = cls.unserialize_attributes(attributes)
        return cls(fields, **attributes)  # type: ignore


    def _write_hdf_dataset(self, hdf_path):
        """ write data to a given hdf5 path `hdf_path` """
        # write attributes of the collection
        for key, value in self.attributes_serialized.items():
            hdf_path.attrs[key] = value
                  
        # write individual fields
        for i, field in enumerate(self.fields):
            field._write_hdf_dataset(hdf_path, f"field_{i}")


    def assert_field_compatible(self, other: FieldBase,
                                accept_scalar: bool = False):
        """ checks whether `other` is compatible with the current field
        
        Args:
            other (FieldBase): Other field this is compared to
            accept_scalar (bool, optional): Determines whether it is acceptable
                that `other` is an instance of
                :class:`~pde.fields.ScalarField`.
        """
        super().assert_field_compatible(other, accept_scalar=accept_scalar)

        # check whether all sub fields are compatible
        if isinstance(other, FieldCollection):
            for f1, f2 in zip(self, other):
                f1.assert_field_compatible(f2, accept_scalar=accept_scalar)
                

    @classmethod
    def scalar_random_uniform(cls, num_fields: int, grid: GridBase,
                              vmin: float = 0, vmax: float = 1,
                              label: Optional[str] = None):
        """ create scalar fields with random values between `vmin` and `vmax`
        
        Args:
            num_fields (int): The number of fields to create
            grid (:class:`~pde.grids.GridBase`):
                Grid defining the space on which the fields are defined
            vmin (float): Smallest random value
            vmax (float): Largest random value
            label (str, optional): Name of the field collection
        """
        return cls([ScalarField.random_uniform(grid, vmin, vmax)
                    for _ in range(num_fields)], label=label)
    
    
    @property
    def attributes(self) -> Dict[str, Any]:
        """ dict: describes the state of the instance (without the data) """
        results = super().attributes
        del results['grid']
        results['fields'] = [f.attributes for f in self.fields]
        return results
    

    @property
    def attributes_serialized(self) -> Dict[str, str]:
        """ dict: serialized version of the attributes """
        results = {}
        for key, value in self.attributes.items():
            if key == 'fields':
                fields = [f.attributes_serialized for f in self.fields]
                results[key] = json.dumps(fields)
            else:
                results[key] = json.dumps(value)
        return results
    
    
    @classmethod
    def unserialize_attributes(cls, attributes: Dict[str, str]) \
            -> Dict[str, Any]:
        """ unserializes the given attributes
        
        Args:
            attributes (dict):
                The serialized attributes
                
        Returns:
            dict: The unserialized attributes
        """
        results = {}
        for key, value in attributes.items():
            if key == 'fields':
                results[key] = [FieldBase.unserialize_attributes(attrs)
                                for attrs in json.loads(value)]
            else:
                results[key] = json.loads(value)
        return results
    
    
    def copy(self, data=None, label: str = None) -> 'FieldCollection':
        """ return a copy of the data, but not of the grid
        
        Args:
            data (:class:`numpy.ndarray`, optional): Data values at the support
                points of the grid that define the field. Note that the data is
                not copied but used directly.
            label (str, optional): Name of the copied field
        """
        if label is None:
            label = self.label
        fields = [f.copy() for f in self.fields]
        # if data is None, the data of the individual fields is copied in their
        # copy() method above. The underlying data is therefore independent from
        # the current field 
        return self.__class__(fields, data=data, label=label)


    def interpolate_to_grid(self, grid: GridBase,
                            method: str = 'numba',
                            fill: float = None,
                            label: Optional[str] = None) -> 'FieldCollection':
        """ interpolate the data of this field collection to another grid.
        
        Args:
            grid (:class:`~pde.grids.GridBase`):
                The grid of the new field onto which the current field is
                interpolated.
            method (str):
                Specifies interpolation method, e.g., 'numba', 'scipy_linear',
                'scipy_nearest' .
            fill (float, optional):
                Determines how values out of bounds are handled. If `None`, a
                `ValueError` is raised when out-of-bounds points are requested.
                Otherwise, the given value is returned.
            label (str, optional):
                Name of the returned field collection
            
        Returns:
            FieldCollection: Interpolated data
        """        
        if label is None:
            label = self.label
        fields = [f.interpolate_to_grid(grid, method=method, fill=fill)
                  for f in self.fields]
        return self.__class__(fields, label=label)        
        

    def smooth(self, sigma: Optional[float] = 1,
               out: Optional['FieldCollection'] = None,
               label: str = None) -> 'FieldCollection':
        """ applies Gaussian smoothing with the given standard deviation

        This function respects periodic boundary conditions of the underlying
        grid, using reflection when no periodicity is specified.
        
        sigma (float, optional):
            Gives the standard deviation of the smoothing in real length units
            (default: 1)
        out (FieldCollection, optional):
            Optional field into which the smoothed data is stored
        label (str, optional):
            Name of the returned field

        Returns:
            Field collection with smoothed data, stored at `out` if given.             
        """
        # allocate memory for storing output
        if out is None:
            out = self.copy(label=label)
        else:
            self.assert_field_compatible(out)
            if label:
                out.label = label
         
        # apply Gaussian smoothing for each axis
        for f_in, f_out in zip(self, out):        
            f_in.smooth(sigma=sigma, out=f_out)
             
        return out   
         
        
    def get_line_data(self, index: int = 0,  # type: ignore
                      **kwargs) -> Dict[str, Any]:
        r""" return data for a line plot of the field
        
        Args:
            index (int): Index of the field whose data is returned
            \**kwargs: Arguments forwarded to the `get_line_data` method
                
        Returns:
            dict: Information useful for performing a line plot of the field
        """
        return self[index].get_line_data(**kwargs)
    
    
    def get_image_data(self, index: int = 0, **kwargs) -> Dict[str, Any]:
        r""" return data for plotting an image of the field

        Args:
            index (int): Index of the field whose data is returned
            \**kwargs: Arguments forwarded to the `get_image_data` method
                
        Returns:
            dict: Information useful for plotting an image of the field
        """
        return self[index].get_image_data(**kwargs)
    
    
    def plot_collection(self,
                        title: Optional[str] = None,
                        tight: bool = True,
                        filename: str = None,
                        show: bool = False,
                        **kwargs):
        r""" visualize all fields by plotting them next to each other
        
        Args:
            title (str):
                Title of the plot. If omitted, the title is chosen automatically
                based on the label the data field.
            tight (bool):
                Whether to call :func:`matplotlib.pyploy.tight_layout`
            filename (str, optional):
                If given, the plot is written to the specified file.
            show (bool):
                Whether to call :func:`matplotlib.pyplot.show`
            \**kwargs:
                Additional keyword arguments are passed to the method
                plotting function of the individual fields.
                
        Returns:
            :class:`matplotlib.figure.Figure`: The figure instance
        """
        import matplotlib.pyplot as plt
        
        # plot the individual panels
        fig, axes = plt.subplots(1, len(self), figsize=(4 * len(self), 3))
        for field, ax in zip(self.fields, axes):
            field.plot(ax=ax, **kwargs)
            
        # set the title above all panels
        fig.suptitle(self.label if title is None else title)
            
        # adjust layout
        if tight:
            fig.tight_layout()
            
        from ..visualization.plotting import finalize_plot
        finalize_plot(fig, filename=filename, show=show)
        return fig
    
    
    def plot_line(self, **kwargs):
        r""" visualize all fields using line plots
        
        Args:
            \**kwargs:
                Supported keyword arguments include `title` to set the title,
                `tight` to adjust the layout, `filename` to write the image to a
                file, and `show` to call :func:`matplotlib.pyplot.show`. These
                are described in :meth:`~FieldCollection.plot_collection`.
                
        Returns:
            :class:`matplotlib.figure.Figure`: The figure instance
        """
        return self.plot_collection(kind='line', **kwargs)
        
        
    def plot_vector(self, **kwargs):
        r""" visualize all fields using vector plots
        
        Args:
            \**kwargs:
                Supported keyword arguments include `title` to set the title,
                `tight` to adjust the layout, `filename` to write the image to a
                file, and `show` to call :func:`matplotlib.pyplot.show`. These
                are described in :meth:`~FieldCollection.plot_collection`.
                
        Returns:
            :class:`matplotlib.figure.Figure`: The figure instance
        """
        return self.plot_collection(kind='vector', **kwargs)
                
    
    def plot_image(self, quantities=None,
                   title: Optional[str] = None,
                   tight: bool = True,
                   filename: str = None,
                   show: bool = True,
                   **kwargs):
        r""" visualize all fields using density plots
        
        Args:
            quantities:
                Determines what exactly is plotted. See
                :class:`~pde.visualization.plotting.ScalarfieldPlot` for details
            title (str):
                Title of the plot. If omitted, the title is chosen automatically
                based on the label the data field.
            tight (bool):
                Whether to call :func:`matplotlib.pyploy.tight_layout`
            filename (str, optional):
                If given, the plot is written to the specified file.
            show (bool):
                Flag setting whether :func:`matplotlib.pyplot.show` is called
            \**kwargs:
                Additional keyword arguments are passed to the plot methods of
                the individual fields
                
        Returns:
            :class:`matplotlib.figure.Figure`: The figure instance
        """
        if title is None:
            title = self.label
            
        # create the plot panels
        from ..visualization.plotting import ScalarFieldPlot
        plot = ScalarFieldPlot(self, quantities=quantities, title=title,
                               tight=tight, show=show)
        
        # save plot to file if requested
        if filename:
            plot.fig.savefig(filename)
            
        return plot.fig
        
        
    def plot(self, kind: str = 'auto', **kwargs):
        r""" visualize the field collection
        
        Args:
            kind (str):
                Determines how to visualize the collection. Supported values are
                `image`,  `line`, or `vector`. Alternatively, `auto` determines
                the best visualization based on each individual field itself.
            \**kwargs:
                All additional keyword arguments are forwarded to the actual
                plotting functions. They include the keyword arguments `title`
                to set the title, `tight` to adjust the layout, `filename` to
                write the image to a file, and `show` to call
                :func:`matplotlib.pyplot.show`. These arguments are described in
                :meth:`~FieldCollection.plot_collection`.
                
        Returns:
            :class:`matplotlib.figure.Figure`: The figure instance
        """
        if kind == 'auto':
            return self.plot_collection(**kwargs)
        elif kind == 'image':
            return self.plot_image(**kwargs)
        elif kind == 'line':
            return self.plot_line(**kwargs)
        elif kind == 'vector':
            return self.plot_vector(**kwargs)
        else:
            raise ValueError(f'Unsupported plot `{kind}`. Possible choices are '
                             '`image`, `line`, `vector`, or `auto`.')
    
